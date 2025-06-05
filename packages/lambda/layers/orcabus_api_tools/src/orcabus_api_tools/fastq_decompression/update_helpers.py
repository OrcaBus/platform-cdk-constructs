#!/usr/bin/env python3

"""
Update helpers for the update script.
"""

# Standard imports
from typing import Optional

# Local imports
from . import fastq_decompression_patch_request
from .globals import JOB_ENDPOINT
from .models import Job, JobStatus


def update_status(
        job_id: str,
        job_status: JobStatus,
        error_message: Optional[str] = None
) -> Job:
    """
    Add QC stats to a fastq_id.

    :param job_id: The job id
    :param job_status: Dictionary of QC stats
    :param error_message: Optional error message
    """
    return fastq_decompression_patch_request(
        f"{JOB_ENDPOINT}/{job_id}",
        params=dict(filter(
            lambda x: x[1] is not None,
            {
                "status": job_status,
                "error_message": error_message
            }.items()
        ))
    )
