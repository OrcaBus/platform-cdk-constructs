from typing import Unpack

from . import data_sharing_patch_request
from .globals import PACKAGE_ENDPOINT, PUSH_ENDPOINT
from .models import PackageObjectDict, JobPatchParameters, PushJobObjectDict


def update_package_status(
        package_id: str,
        **kwargs: Unpack[JobPatchParameters]
) -> PackageObjectDict:
    """
    Add QC stats to a fastq_id.

    :param package_id: The package id
    :param kwargs: JobPatchParameters to update the package with.
    """
    # Raise error if any of the kwargs are not in the FastqListRowQueryParameters
    for key in kwargs.keys():
        if key not in JobPatchParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return data_sharing_patch_request(
        f"{PACKAGE_ENDPOINT}/{package_id}",
        json_data=dict(filter(
            lambda x: x[1] is not None,
            kwargs.items()
        ))
    )


def update_push_job_status(
        push_job_id: str,
        **kwargs: Unpack[JobPatchParameters]
) -> PushJobObjectDict:
    """
    Add push job status to a push job.

    :param push_job_id: The push job id
    :param push_job_status: The push job status to set
    :param error_message: Optional error message
    """
    return data_sharing_patch_request(
        f"{PUSH_ENDPOINT}/{push_job_id}",
        json_data=dict(filter(
            lambda x: x[1] is not None,
            kwargs.items()
        ))
    )
