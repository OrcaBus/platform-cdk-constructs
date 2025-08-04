#!/usr/bin/env python3

"""
Query helpers -

get_job_from_job_id

get_unarchiving_job_list

"""

# Type hints
from typing import List, Unpack, Optional

# Local imports
from . import get_fastq_decompression_request_response_results
from .models import Job, JobStatusType, JobQueryParameters
from .globals import JOB_ENDPOINT


def get_job_from_job_id(job_id: str, **kwargs) -> Job:
    return get_fastq_decompression_request_response_results(f"{JOB_ENDPOINT}/{job_id}", params=kwargs)


def get_decompression_job_list(**kwargs: Unpack[JobQueryParameters]) -> List[Job]:
    """
    Get fastq decompression jobs
    """
    # Raise error if any of the kwargs are not in the FastqListRowQueryParameters
    for key in kwargs.keys():
        if key not in JobQueryParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return get_fastq_decompression_request_response_results(
        JOB_ENDPOINT,
        params=dict(kwargs)
    )


def get_job_list_for_fastq(
        fastq_id: str,
        status: Optional[JobStatusType] = None
) -> List[Job]:
    """
    Check if fastq in job list
    :return:
    """
    return get_decompression_job_list(**dict(filter(
        lambda kv_iter_: kv_iter_[1] is not None,
        {
            "fastqId": fastq_id,
            "status": status
        }.items()
    )))
