#!/usr/bin/env python3

"""
Create the job
"""

from typing import Unpack

from . import icav2_wes_post_request
from .globals import ANALYSES_ENDPOINT
from .models import WESPostRequest, WESResponse


def create_icav2_wes_analysis(
    **kwargs: Unpack[WESPostRequest]
) -> WESResponse:
    """
    Launch an icav2 analysis in the ICAV2 WES API.
    """
    # Confirm param keys are valid
    for key in kwargs.keys():
        if key not in WESPostRequest.__annotations__:
            raise ValueError(f"Invalid parameter key: {key}. Valid keys are: {', '.join(WESPostRequest.__annotations__.keys())}")

    # Confirm param values are valid
    return icav2_wes_post_request(
        ANALYSES_ENDPOINT,
        json_data=dict(**kwargs)
    )
