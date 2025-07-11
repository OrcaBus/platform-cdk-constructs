#!/usr/bin/env python3

"""
Update helpers for the update script.

- add_qc_stats
- add_read_count
- add_ntsm_storage_object / add_ntsm
- add_fastq_pair_storage_object / add_read_set
- detach_fastq_pair_storage_object / detach_read_set
- validate
- invalidate
"""

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
    """
    Add QC stats to a fastq_id.

    :param job_id: The job id
    :param job_status: Dictionary of QC stats
    :param error_message: Optional error message
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
