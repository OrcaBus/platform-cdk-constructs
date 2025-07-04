#!/usr/bin/env python3

"""
Update helpers for the update script.
"""

# Standard imports
from typing import Optional, Dict, Any

# Local imports
from . import fastq_decompression_patch_request
from .globals import JOB_ENDPOINT
from .models import Job, JobStatus, JobOutputType


def update_status(
        job_id: str,
        job_status: JobStatus,
        steps_execution_arn: Optional[str] = None,
        error_message: Optional[str] = None,
        output: Optional[Dict[str, JobOutputType]] = None
) -> Job:
    """
    Add QC stats to a fastq_id.

    :param job_id: The job id
    :param job_status: Dictionary of QC stats
    :param steps_execution_arn:
    :param output:
    :param error_message: Optional error message
    """
    return fastq_decompression_patch_request(
        f"{JOB_ENDPOINT}/{job_id}",
        params=dict(filter(
            lambda x: x[1] is not None,
            {
                "status": job_status,
                "errorMessage": error_message,
                "stepsExecutionArn": steps_execution_arn,
                "output": output
            }.items()
        ))
    )
