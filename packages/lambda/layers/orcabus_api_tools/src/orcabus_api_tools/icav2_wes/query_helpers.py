#!/usr/bin/env python3

from . import get_icav2_wes_request_response_results
from .globals import ANALYSES_ENDPOINT
from .models import WESResponse

# Get the icav2 wes analysis by analysis name
def get_icav2_wes_analysis_by_name(analysis_name: str) -> WESResponse:
    """
    Get the icav2 wes analysis by analysis name
    """
    response_results = get_icav2_wes_request_response_results(
        ANALYSES_ENDPOINT,
        params={"name": analysis_name}
    )

    if not len(response_results) == 1:
        raise ValueError(f"Expected 1 result, got {len(response_results)}")

    return response_results[0]
