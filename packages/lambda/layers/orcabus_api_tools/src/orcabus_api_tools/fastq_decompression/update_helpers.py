#!/usr/bin/env python3

"""Update helpers for the fastq decompression service."""

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
    """Update the status of a decompression job.

    Args:
        job_id: The unique identifier of the job to update.
        **kwargs: Update parameters matching JobUpdateParameters TypedDict.
            Required: status.
            Optional: errorMessage, stepsExecutionArn, output.

    Returns:
        The updated Job object.

    Raises:
        ValueError: If any parameter key is not in JobUpdateParameters.
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
