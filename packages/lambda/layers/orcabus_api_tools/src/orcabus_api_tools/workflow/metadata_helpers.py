#!/usr/bin/env python

"""
Get workflows from library id
"""

# Standard imports
import typing
from typing import List, Optional

# Local imports
from . import get_workflow_request_response_results
from .globals import WORKFLOW_RUN_ENDPOINT
from .models import WorkflowRunDetail
from .workflow_run_helpers import get_workflow_run

# Type hints
if typing.TYPE_CHECKING:
    from ..metadata.models import Library
    from ..fastq.models import Fastq


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


def get_workflows_from_library_id_list(
        library_id_list: List[str],
) -> List[WorkflowRunDetail]:
    """
    Use the query libraries__libraryId to get workflows from a list of library ids
    However, we only collect the workflows that are associated will all libraries in the list,
    This may be useful if given a tumor normal pair and you want to find all workflows associated
    with that specific tumor normal pair
    :param library_id_list:
    :return:
    """

    # If no libraries, then no workflows
    if len(library_id_list) < 1:
        return []

    # Get all workflows from this library id
    all_workflows_intersected = get_workflows_from_library_id(
        library_id_list[0]
    )

    if len(library_id_list) == 1:
        return all_workflows_intersected

    for workflow_iter in all_workflows_intersected:
        # Get all libraries on run
        library_ids_on_run = list(map(
            lambda library_iter_: library_iter_['libraryId'],
            get_libraries_from_workflow_run(workflow_iter['orcabusId'])
        ))

        # If any library is not on the run, then we remove the run.
        if not all(library_id in library_ids_on_run for library_id in library_id_list):
            all_workflows_intersected.remove(workflow_iter)

    return all_workflows_intersected


def get_workflows_from_rgid_list(
        rgid_list: List[str]
) -> List[WorkflowRunDetail]:
    """
    Use the query libraries__rgid to get workflows from a list of rgids
    However, we only collect the workflows that are associated will all rgids in the list,
    This may be useful if given a tumor normal pair and you want to find all workflows associated
    with that specific tumor normal pair
    :param rgid_list:
    :return:
    """
    from ..fastq import get_fastq_by_rgid

    fastq_id_list = list(map(
        lambda rgid_: get_fastq_by_rgid(rgid_)['id'],
        rgid_list
    ))

    if len(fastq_id_list) < 1:
        return []

    all_workflows_intersected = get_workflow_request_response_results(
        WORKFLOW_RUN_ENDPOINT,
        params={
            "readsets": fastq_id_list[0]
        }
    )

    if len(fastq_id_list) == 1:
        return all_workflows_intersected

    for workflow_iter in all_workflows_intersected:
        # Get all libraries on run
        fastqs_on_run = list(map(
            lambda fastq_iter: fastq_iter['id'],
            get_fastqs_on_workflow_run(workflow_iter['orcabusId'])
        ))

        # If any fastq on our list is not on the run, then we remove it
        if not all(fastq_id in fastqs_on_run for fastq_id in fastq_id_list):
            all_workflows_intersected.remove(workflow_iter)

    return all_workflows_intersected


def get_workflow_runs_from_metadata(
        workflow_name: str,
        workflow_version: Optional[str] = None,
        code_version: Optional[str] = None,
        analysis_run_id: Optional[str] = None,
        current_status: Optional[str] = None,
        library_id_list: Optional[List[str]] = None,
        rgid_list: Optional[List[str]] = None,
) -> List[WorkflowRunDetail]:
    """
    Get workflow runs from metadata such as library ids or rgids
    but allow filtering on standard workflow run metadata such as workflow name, version, analysis run id, and current status
    :param workflow_name:
    :param workflow_version:
    :param code_version:
    :param analysis_run_id:
    :param current_status:
    :param library_id_list:
    :param rgid_list:
    :return:
    """

    # Local relative imports
    from .query_helpers import (
        list_workflow_runs
    )

    # Get all workflows for a given workflow name and version
    workflow_run_list = list_workflow_runs(
        workflow_name=workflow_name,
        workflow_version=workflow_version,
        code_version=code_version,
        analysis_run_id=analysis_run_id,
        current_status=current_status,
    )

    # Filter by library id list if provided
    if library_id_list is not None:
        workflow_library_id_list = get_workflows_from_library_id_list(
            library_id_list=library_id_list,
        )
        workflow_run_list = list(filter(
            lambda workflow_run_iter_: (
                workflow_run_iter_['orcabusId'] in list(map(
                    lambda workflow_iter_: workflow_iter_['orcabusId'],
                    workflow_library_id_list
                ))
            ),
            workflow_run_list
        ))

    # Filter by rgid list if provided
    if rgid_list is not None:
        workflow_rgid_list = get_workflows_from_rgid_list(
            rgid_list=rgid_list,
        )
        workflow_run_list = list(filter(
            lambda workflow_run_iter_: (
                workflow_run_iter_['orcabusId'] in list(map(
                    lambda workflow_iter_: workflow_iter_['orcabusId'],
                    workflow_rgid_list
                ))
            ),
            workflow_run_list
        ))

    # Return the filtered list of workflow runs
    return workflow_run_list


def get_readsets_on_workflow_run(
        workflow_run_id: str
) -> List[str]:
    return get_workflow_run(workflow_run_orcabus_id=workflow_run_id).get('readsets', [])


def get_fastqs_on_workflow_run(
        workflow_run_id: str
) -> List['Fastq']:
    # Import locally to prevent circular imports
    from ..fastq import get_fastq

    return list(map(
        lambda fastq_id_iter_: get_fastq(fastq_id_iter_),
        get_readsets_on_workflow_run(workflow_run_id=workflow_run_id)
    ))


def get_libraries_from_workflow_run(
        workflow_run_id: str
) -> List['Library']:
    """
    Get libraries on a workflow run
    :param workflow_run_id:
    :return:
    """
    from ..metadata import get_libraries_from_library_orcabus_id_list

    # Get the library orcabusIds
    library_orcabus_id_list = list(set(
        list(map(
            lambda fastq_obj_iter_: fastq_obj_iter_['library']['orcabusId'],
            get_fastqs_on_workflow_run(workflow_run_id)
        ))
    ))

    return get_libraries_from_library_orcabus_id_list(library_orcabus_id_list=library_orcabus_id_list)
