#!/usr/bin/env python3

# Standard imports
from typing import Dict, Optional

# Local imports
from ..utils.requests_helpers import (
    get_request_response_results,
    get_request,
    get_url
)
from .globals import SEQUENCE_SUBDOMAIN_NAME
from .models import Sequence, SequenceDetail, SampleSheet


def get_sequence_url(endpoint: str) -> str:
    """
    Get the base URL for the sequence api
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint,
        SEQUENCE_SUBDOMAIN_NAME
    )


def get_sequence_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(get_sequence_url(endpoint), params=params)


def get_sequence_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(get_sequence_url(endpoint), params=params)



from .sequence_helpers import (
    get_sequence_object_from_instrument_run_id,
    get_libraries_from_instrument_run_id,
    get_sample_sheet_from_orcabus_id,
    get_library_ids_in_sequence,
    get_sample_sheet_from_instrument_run_id
)

__all__ = [
    "get_sequence_object_from_instrument_run_id",
    "get_libraries_from_instrument_run_id",
    "get_sample_sheet_from_orcabus_id",
    "get_library_ids_in_sequence",
    "get_sample_sheet_from_instrument_run_id",
]


