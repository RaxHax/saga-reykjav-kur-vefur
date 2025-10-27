"""
Job Models

Pydantic models for indexing jobs
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job status enum"""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IndexingOptions(BaseModel):
    """Options for indexing job"""

    batch_size: int = Field(default=100, ge=1, le=1000, description="Batch size for processing")
    image_formats: List[str] = Field(
        default=["jpg", "jpeg", "png", "webp"], description="Supported image formats"
    )
    recursive: bool = Field(default=True, description="Recursively search subdirectories")
    skip_existing: bool = Field(default=True, description="Skip already indexed images")
    extract_metadata: bool = Field(default=True, description="Extract metadata from .txt files")


class JobCreate(BaseModel):
    """Request model for creating a new job"""

    image_folder: str = Field(..., description="Path to folder containing images")
    options: Optional[IndexingOptions] = Field(default_factory=IndexingOptions)


class JobProgress(BaseModel):
    """Job progress information"""

    processed: int = Field(default=0, description="Number of images processed")
    total: int = Field(default=0, description="Total number of images")
    percentage: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress percentage")
    current_file: Optional[str] = Field(default=None, description="Currently processing file")
    eta_seconds: Optional[float] = Field(default=None, description="Estimated time remaining")


class Job(BaseModel):
    """Job model"""

    id: str = Field(..., description="Unique job ID")
    status: JobStatus = Field(default=JobStatus.PENDING, description="Job status")
    image_folder: str = Field(..., description="Path to image folder")
    options: IndexingOptions = Field(default_factory=IndexingOptions)

    progress: JobProgress = Field(default_factory=JobProgress)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    error_message: Optional[str] = None
    logs: List[str] = Field(default_factory=list)

    # Audit fields
    created_by: Optional[str] = Field(default="system", description="User who created the job")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        use_enum_values = True


class JobResponse(BaseModel):
    """Response model for job"""

    id: str
    status: str
    image_folder: str
    progress: JobProgress
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]


class JobListResponse(BaseModel):
    """Response model for list of jobs"""

    jobs: List[JobResponse]
    total: int


class JobLogsResponse(BaseModel):
    """Response model for job logs"""

    job_id: str
    logs: List[str]
    total: int


class JobHistoryEntry(BaseModel):
    """Job history audit entry"""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event: str = Field(..., description="Event type (created, started, paused, etc.)")
    details: Dict[str, Any] = Field(default_factory=dict)
    user: Optional[str] = Field(default=None)


class JobHistoryResponse(BaseModel):
    """Response for job history"""

    job_id: str
    history: List[JobHistoryEntry]
