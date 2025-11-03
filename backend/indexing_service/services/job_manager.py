"""
Job Manager

Manages indexing jobs: creation, execution, monitoring, and lifecycle
"""

import asyncio
import os
import uuid
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

from models.job import Job, JobStatus, JobProgress, JobCreate, JobHistoryEntry
from services.indexer import ImageIndexer
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JobManager:
    """Manages all indexing jobs"""

    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.job_history: Dict[str, List[JobHistoryEntry]] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.indexer: Optional[ImageIndexer] = None
        self.max_concurrent_jobs = int(os.getenv("MAX_CONCURRENT_INDEXING_JOBS", 3))
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize the job manager"""
        logger.info("Initializing Job Manager...")
        self.indexer = ImageIndexer()
        await self.indexer.initialize()
        logger.info("Job Manager initialized successfully")

    async def shutdown(self):
        """Shutdown the job manager"""
        logger.info("Shutting down Job Manager...")

        # Cancel all active tasks
        for task in self.active_tasks.values():
            task.cancel()

        # Wait for tasks to complete
        if self.active_tasks:
            await asyncio.gather(*self.active_tasks.values(), return_exceptions=True)

        # Shutdown indexer
        if self.indexer:
            await self.indexer.shutdown()

        logger.info("Job Manager shut down successfully")

    async def create_job(self, job_create: JobCreate, user: Optional[str] = None) -> Job:
        """Create a new indexing job"""
        async with self._lock:
            # Validate image folder exists
            if not Path(job_create.image_folder).exists():
                raise FileNotFoundError(f"Image folder not found: {job_create.image_folder}")

            # Check concurrent job limit
            running_jobs = sum(1 for job in self.jobs.values() if job.status == JobStatus.RUNNING)
            if running_jobs >= self.max_concurrent_jobs:
                logger.warning(
                    f"Max concurrent jobs ({self.max_concurrent_jobs}) reached. "
                    f"Job will be queued as PENDING."
                )

            # Create job
            job_id = str(uuid.uuid4())
            job = Job(
                id=job_id,
                image_folder=job_create.image_folder,
                options=job_create.options,
                created_by=user or "system",
                status=JobStatus.PENDING,
            )

            self.jobs[job_id] = job
            self.job_history[job_id] = [
                JobHistoryEntry(
                    event="created",
                    details={"folder": job_create.image_folder},
                    user=user,
                )
            ]

            logger.info(f"Job created: {job_id} - {job_create.image_folder}")

            # Auto-start if under concurrent limit
            if running_jobs < self.max_concurrent_jobs:
                await self._start_job_task(job_id)

            return job

    async def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID"""
        return self.jobs.get(job_id)

    async def list_jobs(
        self, status: Optional[JobStatus] = None, limit: int = 100, offset: int = 0
    ) -> List[Job]:
        """List all jobs with optional filtering"""
        jobs = list(self.jobs.values())

        if status:
            jobs = [job for job in jobs if job.status == status]

        # Sort by created_at descending
        jobs.sort(key=lambda x: x.created_at, reverse=True)

        return jobs[offset : offset + limit]

    async def pause_job(self, job_id: str, user: Optional[str] = None) -> Job:
        """Pause a running job"""
        async with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job not found: {job_id}")

            if job.status != JobStatus.RUNNING:
                raise ValueError(f"Job is not running: {job_id}")

            job.status = JobStatus.PAUSED
            job.updated_at = datetime.utcnow()

            self._add_history_entry(
                job_id, JobHistoryEntry(event="paused", user=user)
            )

            logger.info(f"Job paused: {job_id}")
            return job

    async def resume_job(self, job_id: str, user: Optional[str] = None) -> Job:
        """Resume a paused job"""
        async with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job not found: {job_id}")

            if job.status != JobStatus.PAUSED:
                raise ValueError(f"Job is not paused: {job_id}")

            # Check concurrent job limit
            running_jobs = sum(1 for j in self.jobs.values() if j.status == JobStatus.RUNNING)
            if running_jobs >= self.max_concurrent_jobs:
                raise ValueError(
                    f"Cannot resume: max concurrent jobs ({self.max_concurrent_jobs}) reached"
                )

            job.status = JobStatus.RUNNING
            job.updated_at = datetime.utcnow()

            self._add_history_entry(
                job_id, JobHistoryEntry(event="resumed", user=user)
            )

            # Restart the task
            await self._start_job_task(job_id)

            logger.info(f"Job resumed: {job_id}")
            return job

    async def cancel_job(self, job_id: str, user: Optional[str] = None) -> Job:
        """Cancel a job"""
        async with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job not found: {job_id}")

            if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                raise ValueError(f"Job already finished: {job_id}")

            # Cancel the task if running
            if job_id in self.active_tasks:
                self.active_tasks[job_id].cancel()
                del self.active_tasks[job_id]

            job.status = JobStatus.CANCELLED
            job.completed_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()

            self._add_history_entry(
                job_id, JobHistoryEntry(event="cancelled", user=user)
            )

            logger.info(f"Job cancelled: {job_id}")
            return job

    async def get_job_logs(
        self, job_id: str, tail: Optional[int] = None
    ) -> List[str]:
        """Get logs for a job"""
        job = self.jobs.get(job_id)
        if not job:
            raise ValueError(f"Job not found: {job_id}")

        logs = job.logs
        if tail:
            logs = logs[-tail:]

        return logs

    async def get_job_history(self, job_id: str) -> List[JobHistoryEntry]:
        """Get history for a job"""
        if job_id not in self.job_history:
            raise ValueError(f"Job not found: {job_id}")

        return self.job_history[job_id]

    # Private methods

    async def _start_job_task(self, job_id: str):
        """Start a background task for a job"""
        job = self.jobs.get(job_id)
        if not job:
            return

        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow()
        job.updated_at = datetime.utcnow()

        self._add_history_entry(
            job_id, JobHistoryEntry(event="started")
        )

        # Create and store the task
        task = asyncio.create_task(self._run_job(job_id))
        self.active_tasks[job_id] = task

        logger.info(f"Job task started: {job_id}")

    async def _run_job(self, job_id: str):
        """Execute the indexing job"""
        job = self.jobs.get(job_id)
        if not job:
            return

        try:
            self._add_log(job_id, f"Starting indexing job for: {job.image_folder}")

            # Discover images
            self._add_log(job_id, "Discovering images...")
            image_files = await self._discover_images(job)

            if not image_files:
                self._add_log(job_id, "No images found")
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.utcnow()
                return

            job.progress.total = len(image_files)
            self._add_log(job_id, f"Found {len(image_files)} images")

            # Process images in batches
            batch_size = job.options.batch_size
            start_time = time.time()

            for i in range(0, len(image_files), batch_size):
                # Check if paused or cancelled
                if job.status != JobStatus.RUNNING:
                    self._add_log(job_id, f"Job {job.status.value}")
                    break

                batch = image_files[i : i + batch_size]
                self._add_log(job_id, f"Processing batch {i // batch_size + 1}...")

                # Process batch
                for img_path in batch:
                    if job.status != JobStatus.RUNNING:
                        break

                    try:
                        # Index the image using the indexer
                        await self.indexer.index_image(img_path)

                        job.progress.processed += 1
                        job.progress.current_file = str(img_path)

                        # Update progress percentage
                        job.progress.percentage = (
                            job.progress.processed / job.progress.total * 100
                        )

                        # Calculate ETA
                        elapsed = time.time() - start_time
                        if job.progress.processed > 0:
                            avg_time_per_image = elapsed / job.progress.processed
                            remaining = job.progress.total - job.progress.processed
                            job.progress.eta_seconds = avg_time_per_image * remaining

                    except Exception as e:
                        logger.error(f"Error processing {img_path}: {e}")
                        self._add_log(job_id, f"Error: {img_path} - {str(e)}")

                job.updated_at = datetime.utcnow()
                await asyncio.sleep(0)  # Yield control

            # Job completed
            if job.status == JobStatus.RUNNING:
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.utcnow()
                self._add_log(job_id, f"Job completed: {job.progress.processed} images indexed")

                self._add_history_entry(
                    job_id,
                    JobHistoryEntry(
                        event="completed",
                        details={"processed": job.progress.processed},
                    ),
                )

            logger.info(f"Job finished: {job_id} - {job.status.value}")

        except asyncio.CancelledError:
            self._add_log(job_id, "Job cancelled")
            job.status = JobStatus.CANCELLED
            job.completed_at = datetime.utcnow()
            raise

        except Exception as e:
            logger.error(f"Job failed: {job_id} - {e}", exc_info=True)
            self._add_log(job_id, f"Job failed: {str(e)}")
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()

            self._add_history_entry(
                job_id,
                JobHistoryEntry(event="failed", details={"error": str(e)}),
            )

        finally:
            # Clean up task
            if job_id in self.active_tasks:
                del self.active_tasks[job_id]

    async def _discover_images(self, job: Job) -> List[Path]:
        """Discover images in the folder"""
        folder = Path(job.image_folder)
        image_files = []

        for ext in job.options.image_formats:
            if job.options.recursive:
                image_files.extend(folder.rglob(f"*.{ext}"))
            else:
                image_files.extend(folder.glob(f"*.{ext}"))

        return list(set(image_files))  # Remove duplicates

    def _add_log(self, job_id: str, message: str):
        """Add a log entry to a job"""
        job = self.jobs.get(job_id)
        if job:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            job.logs.append(log_entry)

            # Keep only last 1000 log entries
            if len(job.logs) > 1000:
                job.logs = job.logs[-1000:]

    def _add_history_entry(self, job_id: str, entry: JobHistoryEntry):
        """Add a history entry to a job"""
        if job_id not in self.job_history:
            self.job_history[job_id] = []

        self.job_history[job_id].append(entry)
