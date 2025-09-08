#!/usr/bin/env python

"""
Get workflows from library id
"""

# Standard imports
from typing import List

# Local imports
from . import get_workflow_request_response_results
from .globals import WORKFLOW_RUN_ENDPOINT
from .models import WorkflowRunDetail


def get_workflows_from_library_id(library_id: str) -> List[WorkflowRunDetail]:
    """
    Use the query libraries__libraryId to get workflows from a library id
    :param library_id:
    :return:
    """
    return get_workflow_request_response_results(
        WORKFLOW_RUN_ENDPOINT,
        params={
            "libraries__libraryId": library_id
        }
    )


def get_workflows_from_library_id_list(library_id_list: List[str]) -> List[WorkflowRunDetail]:
    """
    Use the query libraries__libraryId to get workflows from a list of library ids
    However, we only collect the workflows that are associated will all libraries in the list,
    This may be useful if given a tumor normal pair and you want to find all workflows associated
    with that specific tumor normal pair
    :param library_id_list:
    :return:
    """

    if len(library_id_list) < 1:
        return []

    all_workflows_intersected = get_workflows_from_library_id(
        library_id_list[0]
    )

    if len(library_id_list) == 1:
        return all_workflows_intersected

    for library_id in library_id_list[1:]:
        workflows_for_library = get_workflows_from_library_id(library_id)
        all_workflows_intersected = list(filter(
            lambda workflow_iter_: workflow_iter_['orcabusId'] in list(map(
                lambda all_workflows_iter_: all_workflows_iter_['orcabusId'],
                all_workflows_intersected
            )),
            workflows_for_library
        ))

    return all_workflows_intersected