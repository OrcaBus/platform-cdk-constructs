#!/usr/bin/env python3

"""
Update helpers for the update script.
"""

# Standard imports
from typing import Unpack

# Local imports
from . import fastq_decompression_patch_request
from .globals import JOB_ENDPOINT
from .models import Job, JobUpdateParameters


def update_status(
        job_id: str,
        **kwargs: Unpack[JobUpdateParameters]
) -> Job:
    """
    Add QC stats to a fastq_id.

    :param job_id:
    :param kwargs: JobUpdateStatusParameters
    """
    # Raise error if any of the kwargs are not in the JobUpdateParameters
    for key in kwargs.keys():
        if key not in JobUpdateParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_decompression_patch_request(
        f"{JOB_ENDPOINT}/{job_id}",
        json_data=dict(filter(
            lambda kv_iter_: kv_iter_[1] is not None,
            kwargs.items()
        ))
    )
