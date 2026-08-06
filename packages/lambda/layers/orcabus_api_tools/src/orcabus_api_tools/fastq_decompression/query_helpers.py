#!/usr/bin/env python3

"""Query helpers for the fastq decompression service.

Functions:
    get_job_from_job_id: Retrieve a specific decompression job by ID.
    get_decompression_job_list: List decompression jobs with optional filters.
    get_job_list_for_fastq: Get all decompression jobs for a specific FASTQ.
"""

# Type hints
from typing import List, Unpack, Optional

# Local imports
from . import get_fastq_decompression_request_response_results
from .models import Job, JobStatusType, JobQueryParameters
from .globals import JOB_ENDPOINT


def get_job_from_job_id(job_id: str, **kwargs) -> Job:
    """Retrieve a decompression job by its ID.

    Args:
        job_id: The unique identifier of the decompression job.
        **kwargs: Additional query parameters.

    Returns:
        The Job object for the specified ID.
    """
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
    """Get all decompression jobs associated with a specific FASTQ.

    Args:
        fastq_id: The FASTQ identifier to search for.
        status: Optional status filter to narrow results.

    Returns:
        A list of Job objects matching the criteria.
    """
    return get_decompression_job_list(**dict(filter(
        lambda kv_iter_: kv_iter_[1] is not None,
        {
            "fastqId": fastq_id,
            "status": status
        }.items()
    )))
