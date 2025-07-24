#!/usr/bin/env python3
from .globals import PACKAGE_ENDPOINT, PUSH_ENDPOINT
from .models import PackageObjectDict, PushJobObjectDict
from . import get_data_sharing_request

def get_package(
        package_id: str,
) -> PackageObjectDict:
    """
    Add QC stats to a fastq_id.

    :param package_id: The package id
    :param kwargs: JobPatchParameters to update the package with.
    """
    return get_data_sharing_request(
        f"{PACKAGE_ENDPOINT}/{package_id}"
    )


def get_push_job(
        push_job_id: str,
) -> PushJobObjectDict:
    """
    Add push job status to a push job.

    :param push_job_id: The push job id
    :param push_job_status: The push job status to set
    :param error_message: Optional error message
    """
    return get_data_sharing_request(
        f"{PUSH_ENDPOINT}/{push_job_id}",
    )