#!/usr/bin/env python3

# Standard imports
import json
import requests
from io import BufferedReader
from typing import Dict, Optional, List, Union, Tuple
from urllib.parse import urlunparse, unquote, urlparse, parse_qs
import logging
from copy import deepcopy
from fastapi.encoders import jsonable_encoder
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

    # Get default request params
    req_params = deepcopy(DEFAULT_REQUEST_PARAMS)

    # Drop any req params that are already in the url
    req_params = dict(filter(
        lambda kv_iter_: kv_iter_[0] not in parse_qs(urlparse(url).query).keys(),
        req_params.items()
    ))

    # Update with params
    req_params.update(
        params if params is not None else {}
    )

    # Iterate through each of the params, if any of the values
    # are boolean, convert them to strings via json.dumps
    req_params = dict(map(
        lambda kv_iter_: (
            kv_iter_[0], (
                json.dumps(kv_iter_[1])
                if isinstance(kv_iter_[1], bool)
                else kv_iter_[1]
            )
        ),
        req_params.items()
    ))

    # Make the request
    response = requests.get(
        url,
        headers=headers,
        params=jsonable_encoder(req_params)
    )

    response.raise_for_status()

    response_json = response.json()

    if 'links' not in response_json.keys():
        return [response_json]

    if 'next' in response_json['links'].keys() and response_json['links']['next'] is not None:
        return response_json['results'] + get_request_response_results(unquote(response_json['links']['next']))
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


def patch_request(
        url: str,
        json_data: Optional[Union[Dict, List]] = None,
        params: Optional[Union[List | Dict]] = None
) -> Dict:
    # Get authorization header
    headers = {
        "Authorization": f"Bearer {get_orcabus_token()}"
    }

    if json_data is not None:
       headers.update({
           "Content-Type": "application/json"
       })

    # Make the request
    response = requests.patch(
        url,
        headers=headers,
        params=params,
        json=json_data
    )

    try:
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"Error {e} - {response.text}") from e

    return response.json()


def post_request(
        url: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        files:  Optional[Dict[str, Tuple[str, BufferedReader, str]]] = None,
) -> Dict:
    """
    Run post request against the fastq endpoint
    :param json_data:
    :param url:
    :param params:
    :param files:
    :return:
    """
    # Get authorization header
    headers = {
        "Authorization": f"Bearer {get_orcabus_token()}",
    }

    # Set content type headers
    if files is not None:
        # Let requests set the content type for multipart
        pass
    elif json_data is not None:
       headers.update({
           "Content-Type": "application/json"
       })

    # Make the request
    response = requests.post(
        url,
        headers=headers,
        json=json_data,
        params=params,
        files=files,
    )

    try:
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(f"Error {e} - {response.text}") from e

    return response.json()
