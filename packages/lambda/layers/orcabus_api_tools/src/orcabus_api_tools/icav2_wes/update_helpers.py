#!/usr/bin/env python3
from typing import Optional

from . import icav2_wes_patch_request
from .globals import ANALYSES_ENDPOINT
from .models import WESResponse

# Get the icav2 wes analysis by analysis name
def update_icav2_wes_analysis_status(
        icav2_wes_orcabus_id: str,
        status: str,
        icav2_analysis_id: Optional[str] = None
) -> WESResponse:
    """
    Get the icav2 wes analysis by analysis name
    """
    return icav2_wes_patch_request(
        f"{ANALYSES_ENDPOINT}/{icav2_wes_orcabus_id}",
        params=dict(filter(
            lambda kv_iter_: kv_iter_[1] is not None,
            {
                "status": status,
                "icav2AnalysisId": icav2_analysis_id
            }.items()
        ))
    )
