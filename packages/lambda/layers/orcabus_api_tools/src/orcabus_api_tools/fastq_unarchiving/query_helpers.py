#!/usr/bin/env python3

"""
Query helpers -

get_job_from_job_id

get_unarchiving_job_list

"""

# Type hints
from typing import List, Unpack

# Local imports
from . import get_fastq_unarchiving_request_response_results
from .models import Job, JobStatusType, JobQueryParameters

from .globals import JOB_ENDPOINT


def get_job_from_job_id(job_id: str, **kwargs) -> Job:
    """Retrieve an unarchiving job by its ID.

    Args:
        job_id: The unique identifier of the unarchiving job.
        **kwargs: Additional query parameters.

    Returns:
        The Job object for the specified ID.
    """
    return get_fastq_unarchiving_request_response_results(f"{JOB_ENDPOINT}/{job_id}", params=kwargs)


def get_unarchiving_job_list(**kwargs: Unpack[JobQueryParameters]) -> List[Job]:
    """
    Get fastq unarchiving jobs
    """
    # Raise error if any of the kwargs are not in the FastqListRowQueryParameters
    for key in kwargs.keys():
        if key not in JobQueryParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return get_fastq_unarchiving_request_response_results(
        JOB_ENDPOINT,
        params=dict(kwargs)
    )


def get_job_list_for_fastq(
        fastq_id: str,
        job_status: JobStatusType
) -> List[Job]:
    """Get all unarchiving jobs for a specific FASTQ with the given status.

    Args:
        fastq_id: The FASTQ identifier to search for.
        job_status: The job status to filter by.

    Returns:
        A list of Job objects matching the criteria.
    """
    return get_unarchiving_job_list(
        fastqId=fastq_id,
        status=job_status
    )
