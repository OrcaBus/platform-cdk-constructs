#!/usr/bin/env python3

"""
Create the job
"""

from typing import List, Optional, Unpack

from . import fastq_decompression_post_request
from .globals import JOB_ENDPOINT
from .models import Job, JobType, JobCreateParameters


def create_job(
    **kwargs: Unpack[JobCreateParameters]
) -> Job:
    """
    Create the job
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
        params=non_null_kwargs
    )
