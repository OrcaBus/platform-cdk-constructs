#!/usr/bin/env python3

"""Query helpers for the data sharing service."""

from .globals import PACKAGE_ENDPOINT, PUSH_ENDPOINT
from .models import PackageObjectDict, PushJobObjectDict
from . import get_data_sharing_request

def get_package(
        package_id: str,
) -> PackageObjectDict:
    """Retrieve a data sharing package by its ID.

    Args:
        package_id: The package identifier.

    Returns:
        The PackageObjectDict for the specified package.
    """
    return get_data_sharing_request(
        f"{PACKAGE_ENDPOINT}/{package_id}"
    )


def get_push_job(
        push_job_id: str,
) -> PushJobObjectDict:
    """Retrieve a push job by its ID.

    Args:
        push_job_id: The push job identifier.

    Returns:
        The PushJobObjectDict for the specified push job.
    """
    return get_data_sharing_request(
        f"{PUSH_ENDPOINT}/{push_job_id}",
    )