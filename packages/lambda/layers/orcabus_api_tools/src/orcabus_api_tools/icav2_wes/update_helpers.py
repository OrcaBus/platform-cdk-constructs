#!/usr/bin/env python3
from typing import Unpack

from . import icav2_wes_patch_request
from .globals import ANALYSES_ENDPOINT
from .models import WESResponse, WESPatchRequest


# Get the icav2 wes analysis by analysis name
def update_icav2_wes_analysis_status(
        icav2_wes_orcabus_id: str,
        **kwargs: Unpack[WESPatchRequest]
) -> WESResponse:
    """
    Get the icav2 wes analysis by analysis name
    """
    # Confirm param keys are valid
    for key in kwargs.keys():
        if key not in WESPatchRequest.__annotations__:
            raise ValueError(
                f"Invalid parameter key: {key}. "
                f"Valid keys are: {', '.join(WESPatchRequest.__annotations__.keys())}"
            )

    # Return the patch request
    return icav2_wes_patch_request(
        f"{ANALYSES_ENDPOINT}/{icav2_wes_orcabus_id}",
        json_data=dict(filter(
            lambda kv_iter_: kv_iter_[1] is not None,
            kwargs.items()
        ))
    )
