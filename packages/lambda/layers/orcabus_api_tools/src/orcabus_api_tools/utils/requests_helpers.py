#!/usr/bin/env python3
from typing import Dict, Optional, List
from urllib.parse import urlunparse

# Standard imports
import requests
import logging
from copy import deepcopy

from requests import HTTPError

# Locals
from .aws_helpers import (
    get_orcabus_token, get_hostname
)

# Globals
DEFAULT_REQUEST_PARAMS = {
    "rowsPerPage": 1000
}

# Set logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_url(
        endpoint: str,
        subdomain: str
) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    # Get the hostname
    hostname = get_hostname()

    return str(urlunparse((
        "https",
        ".".join([subdomain, hostname]),
        endpoint,
        None, None, None
    )))


def get_request_response_results(url: str, params: Optional[Dict] = None) -> List[Dict]:
    """
    Run get response against the Metadata endpoint
    :param url:
    :param params:
    :return:
    """
    # Get authorization header
    headers = {
        "Authorization": f"Bearer {get_orcabus_token()}"
    }

    req_params = deepcopy(DEFAULT_REQUEST_PARAMS)

    req_params.update(
        params if params is not None else {}
    )


    # Make the request
    response = requests.get(
        url,
        headers=headers,
        params=req_params
    )

    response.raise_for_status()

    response_json = response.json()

    if 'links' not in response_json.keys():
        return [response_json]

    if 'next' in response_json['links'].keys() and response_json['links']['next'] is not None:
        return response_json['results'] + get_request_response_results(response_json['links']['next'])
    return response_json['results']


def get_request(url: str, params: Optional[Dict] = None) -> Dict:
    # Get authorization header
    headers = {
        "Authorization": f"Bearer {get_orcabus_token()}"
    }

    # Make the request
    response = requests.get(
        url,
        headers=headers,
        params=params if params is not None else {}
    )

    try:
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"Error {e} - {response.text}") from e

    return response.json()


def patch_request(url: str, params: Optional[Dict] = None) -> Dict:
    # Get authorization header
    headers = {
        "Authorization": f"Bearer {get_orcabus_token()}"
    }

    req_params = deepcopy(DEFAULT_REQUEST_PARAMS)

    req_params.update(
        params if params is not None else {}
    )

    # Make the request
    response = requests.patch(
        url,
        headers=headers,
        json=req_params
    )

    try:
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"Error {e} - {response.text}") from e

    return response.json()


def post_request(url: str, params: Optional[Dict] = None) -> Dict:
    """
    Run post request against the fastq endpoint
    :param url:
    :param params:
    :return:
    """
    # Get authorization header
    headers = {
        "Authorization": f"Bearer {get_orcabus_token()}"
    }

    req_params = deepcopy(DEFAULT_REQUEST_PARAMS)

    req_params.update(
        params if params is not None else {}
    )

    # Make the request
    response = requests.post(
        url,
        headers=headers,
        json=req_params
    )

    try:
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"Error {e} - {response.text}") from e

    return response.json()
