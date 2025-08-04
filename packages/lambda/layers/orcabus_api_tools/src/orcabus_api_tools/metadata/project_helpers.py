#!/usr/bin/env python3

"""
Helpers for using the project API endpoint
"""

# Standard imports
from typing import List
from requests import HTTPError


# Local imports
from . import get_metadata_request_response_results, get_item_objs_from_item_id_list
from .errors import ProjectNotFoundError
from .globals import PROJECT_ENDPOINT, LIBRARY_ENDPOINT, ORCABUS_ULID_REGEX_MATCH
from .models import Project, Library



def get_project_from_project_id(project_id: str) -> Project:
    """
    Get project from the project id
    :param project_id:
    :return:
    """
    # We have an internal id, convert to int
    params = {
        "projectId": project_id
    }

    # Get project
    try:
        query_results = get_metadata_request_response_results(PROJECT_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError) as e:
        raise ProjectNotFoundError(
            project_id=project_id,
        )


def get_projects_list_from_project_id_list(project_id_list: List[str], accept_missing: bool = False) -> List[Project]:
    """
    Get project from the project id
    :param project_id_list:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda project_iter_: Project(**project_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=project_id_list,
            item_identifier="projectId",
            endpoint=PROJECT_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_project_orcabus_id_from_project_id(project_id: str) -> str:
    return get_project_from_project_id(project_id)["orcabusId"]


def coerce_project_id_or_orcabus_id_to_project_orcabus_id(id_: str) -> str:
    if ORCABUS_ULID_REGEX_MATCH.match(id_):
        return id_
    else :
        return get_project_orcabus_id_from_project_id(id_)


def get_project_from_project_orcabus_id(project_orcabus_id: str) -> Project:
    """
    Get project from the project id
    :param project_orcabus_id:
    :return:
    """
    params = {
        "orcabusId": project_orcabus_id.split(".")[1]
    }

    # Get project
    try:
        query_results = get_metadata_request_response_results(PROJECT_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError) as e:
        raise ProjectNotFoundError(
            project_id=project_orcabus_id,
        )


def get_projects_list_from_project_orcabus_id_list(project_orcabus_id_list: List[str], accept_missing: bool = False) -> List[Project]:
    """
    Get project from the project id
    :param project_orcabus_id_list:
    :param accept_missing:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda project_iter_: Project(**project_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=project_orcabus_id_list,
            item_identifier="orcabusId",
            endpoint=PROJECT_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_all_projects() -> List[Project]:
    """
    Get all projects
    :return:
    """
    return get_metadata_request_response_results(PROJECT_ENDPOINT)


def list_libraries_in_project(project_orcabus_id: str) -> List[Library]:
    """
    List all libraries in a project
    Use the projectSet__orcabusId query

    :return:
    """
    params = {
        "projectSet__orcabusId": project_orcabus_id
    }

    return get_metadata_request_response_results(LIBRARY_ENDPOINT, params)
