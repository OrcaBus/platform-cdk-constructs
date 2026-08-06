#!/usr/bin/env python3

"""Update helpers for the fastq unarchiving service."""

# Standard imports
from typing import Optional

# Local imports
from . import fastq_unarchiving_patch_request
from .globals import JOB_ENDPOINT
from .models import Job, JobStatusType


def update_status(
        job_id: str,
        job_status: JobStatusType,
        error_message: Optional[str] = None
) -> Job:
    """Update the status of an unarchiving job.

    Args:
        job_id: The unique identifier of the job to update.
        job_status: The new status to set.
        error_message: Optional error message if the job failed.

    Returns:
        The updated Job object.
    """
    return fastq_unarchiving_patch_request(
        f"{JOB_ENDPOINT}/{job_id}",
        json_data=dict(filter(
            lambda x: x[1] is not None,
            {
                "status": job_status,
                "error_message": error_message
            }.items()
        ))
    )
