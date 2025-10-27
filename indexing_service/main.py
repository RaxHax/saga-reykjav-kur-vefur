"""
Indexing Service - FastAPI Application

A dedicated service for managing image indexing jobs separate from the main Flask app.
Features:
- Start/pause/resume/cancel indexing jobs
- Real-time progress tracking
- Job scheduling and queuing
- Audit logging
- RESTful API for job management
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.routes import jobs_router, health_router
from services.job_manager import JobManager
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

# Initialize job manager (singleton)
job_manager = JobManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Indexing Service...")
    # Startup: Initialize job manager
    await job_manager.initialize()
    logger.info("Indexing Service started successfully")

    yield

    # Shutdown: Clean up resources
    logger.info("Shutting down Indexing Service...")
    await job_manager.shutdown()
    logger.info("Indexing Service stopped")


# Create FastAPI app
app = FastAPI(
    title="SAGA Reykjavík Indexing Service",
    description="Image indexing job management service with real-time progress tracking",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])


# Make job_manager available to routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "SAGA Reykjavík Indexing Service",
        "version": "1.0.0",
        "status": "operational",
    }


# Dependency to get job manager
def get_job_manager() -> JobManager:
    """Dependency to inject job manager"""
    return job_manager


# Export for use in routes
__all__ = ["app", "get_job_manager"]
