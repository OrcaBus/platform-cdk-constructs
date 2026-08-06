#!/usr/bin/env python3

"""
Create the job
"""

from typing import Unpack

from . import fastq_decompression_post_request
from .globals import JOB_ENDPOINT
from .models import Job, JobCreateParameters


def create_job(
    **kwargs: Unpack[JobCreateParameters]
) -> Job:
    """Create a new fastq decompression job.

    Args:
        **kwargs: Job creation parameters matching JobCreateParameters TypedDict.
            Required: fastqIdList, jobType.
            Optional: maxReads, outputUriPrefix, sampling, noSplitByLane, fileUriByFastqIdMap.

    Returns:
        The created Job object with its assigned ID and initial status.

    Raises:
        ValueError: If any parameter key is not in JobCreateParameters.
    """

    # Raise error if any of the kwargs are not in the FastqListRowQueryParameters
    for key in kwargs.keys():
        if key not in JobCreateParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    non_null_kwargs = dict(filter(
        lambda kv_iter_: kv_iter_[1] is not None,
        kwargs.items()
    ))

    return fastq_decompression_post_request(
        JOB_ENDPOINT,
        json_data=non_null_kwargs
    )
