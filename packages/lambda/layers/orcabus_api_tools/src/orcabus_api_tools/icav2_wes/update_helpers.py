#!/usr/bin/env python3

from . import icav2_wes_patch_request
from .globals import ANALYSES_ENDPOINT
from .models import WESResponse

# Get the icav2 wes analysis by analysis name
def update_icav2_wes_analysis_status(
        icav2_wes_orcabus_id: str,
        status: str
) -> WESResponse:
    """
    Get the icav2 wes analysis by analysis name
    """
    response_results = icav2_wes_patch_request(
        f"{ANALYSES_ENDPOINT}/{icav2_wes_orcabus_id}",
        params={"status": status}
    )

    if not len(response_results) == 1:
        raise ValueError(f"Expected 1 result, got {len(response_results)}")

    return response_results[0]
