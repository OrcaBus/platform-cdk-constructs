"""Update helpers for the data sharing service."""

from typing import Unpack

from . import data_sharing_patch_request
from .globals import PACKAGE_ENDPOINT, PUSH_ENDPOINT
from .models import PackageObjectDict, JobPatchParameters, PushJobObjectDict


def update_package_status(
        package_id: str,
        **kwargs: Unpack[JobPatchParameters]
) -> PackageObjectDict:
    """Update the status of a data sharing package.

    Args:
        package_id: The package identifier.
        **kwargs: Update parameters matching JobPatchParameters TypedDict.

    Returns:
        The updated PackageObjectDict.

    Raises:
        ValueError: If any parameter key is not in JobPatchParameters.
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
    """Update the status of a push job.

    Args:
        push_job_id: The push job identifier.
        **kwargs: Update parameters matching JobPatchParameters TypedDict.

    Returns:
        The updated PushJobObjectDict.
    """
    return data_sharing_patch_request(
        f"{PUSH_ENDPOINT}/{push_job_id}",
        json_data=dict(filter(
            lambda x: x[1] is not None,
            kwargs.items()
        ))
    )
