"""
API Routes for Indexing Service
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List

from models.job import (
    Job,
    JobCreate,
    JobResponse,
    JobListResponse,
    JobLogsResponse,
    JobStatus,
    JobHistoryResponse,
)
from services.job_manager import JobManager

# Routers
health_router = APIRouter()
jobs_router = APIRouter()


# Dependency to get job manager (will be injected from main.py)
async def get_job_manager() -> JobManager:
    """Dependency to get the job manager instance"""
    from main import get_job_manager as _get_manager

    return _get_manager()


# =============================================================================
# Health Endpoints
# =============================================================================


@health_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "indexing",
        "timestamp": "2025-01-01T00:00:00Z",
    }


# =============================================================================
# Job Management Endpoints
# =============================================================================


@jobs_router.post("/start", response_model=JobResponse)
async def start_job(
    job_create: JobCreate,
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Start a new indexing job

    Creates and starts a new background indexing job for the specified image folder.
    """
    try:
        job = await job_manager.create_job(job_create)
        return _job_to_response(job)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@jobs_router.get("/{job_id}/status", response_model=JobResponse)
async def get_job_status(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Get the status of a specific job

    Returns current progress, status, and statistics for the job.
    """
    job = await job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")

    return _job_to_response(job)


@jobs_router.get("", response_model=JobListResponse)
async def list_jobs(
    status: Optional[JobStatus] = Query(None, description="Filter by job status"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of jobs to return"),
    offset: int = Query(0, ge=0, description="Number of jobs to skip"),
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    List all jobs with optional filtering

    Returns a paginated list of jobs, optionally filtered by status.
    """
    jobs = await job_manager.list_jobs(status=status, limit=limit, offset=offset)
    return JobListResponse(
        jobs=[_job_to_response(job) for job in jobs],
        total=len(job_manager.jobs),
    )


@jobs_router.post("/{job_id}/pause", response_model=JobResponse)
async def pause_job(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Pause a running job

    Pauses the execution of a running job. The job can be resumed later.
    """
    try:
        job = await job_manager.pause_job(job_id)
        return _job_to_response(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pause job: {str(e)}")


@jobs_router.post("/{job_id}/resume", response_model=JobResponse)
async def resume_job(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Resume a paused job

    Resumes the execution of a previously paused job.
    """
    try:
        job = await job_manager.resume_job(job_id)
        return _job_to_response(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume job: {str(e)}")


@jobs_router.post("/{job_id}/cancel", response_model=JobResponse)
async def cancel_job(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Cancel a job

    Cancels the execution of a job. This action cannot be undone.
    """
    try:
        job = await job_manager.cancel_job(job_id)
        return _job_to_response(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel job: {str(e)}")


@jobs_router.get("/{job_id}/logs", response_model=JobLogsResponse)
async def get_job_logs(
    job_id: str,
    tail: Optional[int] = Query(None, ge=1, le=1000, description="Number of recent log lines"),
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Get logs for a job

    Returns the log entries for a specific job, optionally limited to recent entries.
    """
    try:
        logs = await job_manager.get_job_logs(job_id, tail=tail)
        return JobLogsResponse(
            job_id=job_id,
            logs=logs,
            total=len(logs),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")


@jobs_router.get("/history", response_model=List[JobHistoryResponse])
async def get_jobs_history(
    limit: int = Query(10, ge=1, le=100),
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Get history of all jobs

    Returns audit trail for all jobs with event history.
    """
    # Get recent jobs
    jobs = await job_manager.list_jobs(limit=limit)

    history_responses = []
    for job in jobs:
        try:
            history = await job_manager.get_job_history(job.id)
            history_responses.append(
                JobHistoryResponse(
                    job_id=job.id,
                    history=history,
                )
            )
        except Exception:
            continue

    return history_responses


@jobs_router.get("/{job_id}/history", response_model=JobHistoryResponse)
async def get_job_history(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    """
    Get history for a specific job

    Returns the complete audit trail for a job.
    """
    try:
        history = await job_manager.get_job_history(job_id)
        return JobHistoryResponse(
            job_id=job_id,
            history=history,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


# =============================================================================
# Helper Functions
# =============================================================================


def _job_to_response(job: Job) -> JobResponse:
    """Convert Job model to JobResponse"""
    return JobResponse(
        id=job.id,
        status=job.status.value,
        image_folder=job.image_folder,
        progress=job.progress,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message,
    )
