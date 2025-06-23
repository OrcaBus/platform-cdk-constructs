#!/usr/bin/env python3

"""
Create the job
"""

from typing import List, Optional

from . import fastq_decompression_post_request
from .globals import JOB_ENDPOINT
from .models import Job, JobType


def create_job(
        fastq_id_list: List[str],
        output_uri_prefix: str = None,
        job_type: Optional[JobType] = None,
) -> Job:
    """
    Create the job
    """
    if job_type is None:
        job_type = 'FASTQ_DECOMPRESSION'

    return fastq_decompression_post_request(
        JOB_ENDPOINT,
        params={
            "fastqIdList": fastq_id_list,
            "jobType": job_type,
            "outputUriPrefix": output_uri_prefix,
        }
    )


