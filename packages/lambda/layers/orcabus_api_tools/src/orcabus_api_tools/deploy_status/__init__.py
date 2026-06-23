#!/usr/bin/env python3

"""
Deploy Status toolkit
"""

# Shared imports
from ..utils.requests_helpers import get_url

# Local imports
from .globals import DEPLOY_STATUS_SUBDOMAIN_NAME


def get_deploy_status_endpoint(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint,
        DEPLOY_STATUS_SUBDOMAIN_NAME
    )


# Exported functions
from .query_helpers import get_all_stacks_summary

__all__ = [
    "get_all_stacks_summary"
]
