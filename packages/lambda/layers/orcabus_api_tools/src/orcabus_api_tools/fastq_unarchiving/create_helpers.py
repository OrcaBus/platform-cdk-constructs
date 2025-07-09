#!/usr/bin/env python3

"""
Create the job
"""

from typing import List, Optional

from . import fastq_unarchiving_post_request
from .globals import JOB_ENDPOINT
from .models import Job, JobType


def create_job(fastq_ids: List[str], job_type: Optional[JobType] = None) -> Job:
    """
    Create the job
    """
    if job_type is None:
        job_type = 'S3_UNARCHIVING'

    return fastq_unarchiving_post_request(
        JOB_ENDPOINT,
        params={
            "fastqIds": fastq_ids,
            "jobType": job_type
        }
    )
