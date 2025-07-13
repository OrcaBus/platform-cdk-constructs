# FIMXE Implement the following imports
from typing import Optional, Dict

from .globals import DATA_SHARING_SUBDOMAIN_NAME
from ..utils.requests_helpers import get_url, get_request, get_request_response_results, patch_request


# Get url for the subdomain
def get_data_sharing_url(endpoint: str) -> str:
    """
    Get the URL for the data sharing endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint=endpoint,
        subdomain=DATA_SHARING_SUBDOMAIN_NAME,
    )


# Wrappers
def get_data_sharing_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(
        url=get_data_sharing_url(endpoint),
        params=params
    )


def get_data_sharing_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(
        url=get_data_sharing_url(endpoint),
        params=params
    )


def data_sharing_patch_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    return patch_request(
        url=get_data_sharing_url(endpoint),
        json_data=json_data
    )


def data_sharing_post_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    return patch_request(
        url=get_data_sharing_url(endpoint),
        json_data=json_data
    )


from .update_helpers import (
    update_package_status,
    update_push_job_status,
)

__all__ = [
    "update_package_status",
    "update_push_job_status",
]