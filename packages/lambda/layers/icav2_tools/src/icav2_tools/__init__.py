#!/usr/bin/env python

from .aws_helpers import get_icav2_access_token
from os import environ
from .globals import ICAV2_BASE_URL


def set_icav2_env_vars():
    """
    Set the environment variables for the ICAV2 API
    :return:
    """
    environ["ICAV2_ACCESS_TOKEN"] = get_icav2_access_token()
    environ["ICAV2_BASE_URL"] = ICAV2_BASE_URL


__all__ = [
    "set_icav2_env_vars"
]
