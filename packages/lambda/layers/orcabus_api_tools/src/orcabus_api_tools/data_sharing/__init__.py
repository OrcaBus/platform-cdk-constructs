# FIMXE Implement the following imports
from typing import Optional, List, Dict, TypedDict, NotRequired

from .globals import DATA_SHARING_SUBDOMAIN_NAME
from ..utils.requests_helpers import (
    get_url,
    get_request,
    get_request_response_results,
    patch_request,
    post_request,
)


# Get url for the subdomain
def get_data_sharing_url(endpoint: str) -> str:
    """
    Get the URL for the data sharing endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint=endpoint,
        subdomain=DATA_SHARING_SUBDOMAIN_NAME,
    )


# Wrappers
def get_data_sharing_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return get_request(url=get_data_sharing_url(endpoint), params=params)


def get_data_sharing_request_response_results(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return get_request_response_results(
        url=get_data_sharing_url(endpoint), params=params
    )


def data_sharing_patch_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    return patch_request(url=get_data_sharing_url(endpoint), json_data=json_data)


def data_sharing_post_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    return patch_request(url=get_data_sharing_url(endpoint), json_data=json_data)


# Models
class PackageRequestDict(TypedDict):
    libraryIdList: List[str]
    dataTypeList: List[str]
    portalRunIdList: NotRequired[List[str]]
    defrostArchivedFastqs: NotRequired[bool]
    useWorkflowFilters: NotRequired[bool]
    instrumentRunIdList: NotRequired[List[str]]


def create_package(
    package_name: str,
    package_request: PackageRequestDict,
) -> Dict:
    response = post_request(
        json_data={
            "packageName": package_name,
            "packageRequest": package_request,
        },
        url=get_data_sharing_url("/api/v1/package"),
    )

    return response


def push_package(
    package_id: str,
    location_uri: str,
) -> Dict:

    response = post_request(
        json_data={
            "shareDestination": location_uri,
        },
        url=get_data_sharing_url(f"/api/v1/package/{package_id}:push"),
    )

    return response


from .query_helpers import get_package, get_push_job

from .update_helpers import (
    update_package_status,
    update_push_job_status,
)

__all__ = [
    # Get helpers
    "get_package",
    "get_push_job",
    # Push job helpers
    "push_package",
    "update_package_status",
    "update_push_job_status",
    # Package helpers
    "create_package",
]
