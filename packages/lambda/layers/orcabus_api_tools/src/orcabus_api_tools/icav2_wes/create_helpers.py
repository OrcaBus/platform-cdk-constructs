#!/usr/bin/env python3

"""
Create the job
"""

from typing import Unpack

from . import icav2_wes_post_request
from .globals import ANALYSES_ENDPOINT
from .models import WESRequest, WESResponse


def create_icav2_wes_analysis(
    **kwargs: Unpack[WESRequest]
) -> WESResponse:
    """
    Launch an icav2 analysis in the ICAV2 WES API.
    """
    # Confirm param keys are valid
    for key in kwargs.keys():
        if key not in WESRequest.__annotations__:
            raise ValueError(f"Invalid parameter key: {key}. Valid keys are: {', '.join(WESRequest.__annotations__.keys())}")

    # Confirm param values are valid
    return icav2_wes_post_request(
        ANALYSES_ENDPOINT,
        params=dict(**kwargs)
    )
