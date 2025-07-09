from typing import Optional

from . import data_sharing_patch_request
from .globals import PACKAGE_ENDPOINT, PUSH_ENDPOINT
from .models import PackageStatusType, PackageObject, PushJobStatusType


def update_package_status(
        package_id: str,
        package_status: PackageStatusType,
        error_message: Optional[str] = None
) -> PackageObject:
    """
    Add QC stats to a fastq_id.

    :param package_id: The package id
    :param package_status: The package status to set
    :param error_message: Optional error message
    """
    return data_sharing_patch_request(
        f"{PACKAGE_ENDPOINT}/{package_id}",
        params=dict(filter(
            lambda x: x[1] is not None,
            {
                "status": package_status,
                "error_message": error_message
            }.items()
        ))
    )


def update_push_job_status(
        push_job_id: str,
        push_job_status: PushJobStatusType,
        error_message: Optional[str] = None
) -> PackageObject:
    """
    Add push job status to a push job.

    :param push_job_id: The push job id
    :param push_job_status: The push job status to set
    :param error_message: Optional error message
    """
    return data_sharing_patch_request(
        f"{PUSH_ENDPOINT}/{push_job_id}",
        params=dict(filter(
            lambda x: x[1] is not None,
            {
                "status": push_job_status,
                "error_message": error_message
            }.items()
        ))
    )
