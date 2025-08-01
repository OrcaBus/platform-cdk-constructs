#!/usr/bin/env python3

# Imports
from typing import Optional, Dict

from .globals import ICAV2_WES_SUBDOMAIN_NAME
from .models import WESPostRequest
from ..utils.requests_helpers import (
    get_request, get_url, patch_request, get_request_response_results, post_request
)


# Wrappers
def get_icav2_wes_url(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint=endpoint,
        subdomain=ICAV2_WES_SUBDOMAIN_NAME,
    )


def get_icav2_wes_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(
        url=get_icav2_wes_url(endpoint),
        params=params
    )


def get_icav2_wes_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(
        url=get_icav2_wes_url(endpoint),
        params=params
    )


def icav2_wes_patch_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    return patch_request(
        url=get_icav2_wes_url(endpoint),
        json_data=json_data
    )


def icav2_wes_post_request(
    endpoint: str,
    json_data: Dict
):
    # Confirm param keys are valid
    return post_request(
        url=get_icav2_wes_url(endpoint),
        json_data=json_data
    )


# Set all
from .create_helpers import create_icav2_wes_analysis
from .query_helpers import get_icav2_wes_analysis_by_name
from .update_helpers import update_icav2_wes_analysis_status

__all__ = [
    # Models
    'WESPostRequest',
    # Launch helpers
    'create_icav2_wes_analysis',
    # Query helpers
    'get_icav2_wes_analysis_by_name',
    # Update helpers
    'update_icav2_wes_analysis_status'
]
