#!/usr/bin/env python3

"""
Create the job
"""

from typing import List, Optional

from . import fastq_unarchiving_post_request
from .globals import JOB_ENDPOINT
from .models import Job, JobType


def create_job(fastq_ids: List[str], job_type: Optional[JobType] = None) -> Job:
    """Create a new fastq unarchiving job to restore files from S3 Glacier.

    Args:
        fastq_ids: List of FASTQ identifiers to restore.
        job_type: The type of unarchiving job. Defaults to 'S3_UNARCHIVING'.

    Returns:
        The created Job object with its assigned ID and initial status.
    """
    if job_type is None:
        job_type = 'S3_UNARCHIVING'

    return fastq_unarchiving_post_request(
        JOB_ENDPOINT,
        json_data={
            "fastqIds": fastq_ids,
            "jobType": job_type
        }
    )
