#!/usr/bin/env python3
from functools import reduce
from itertools import batched
from operator import concat
# Standard imports
from typing import Dict, List, Any
from urllib.error import HTTPError

# Util imports
from ..utils.requests_helpers import (
    get_request_response_results, get_url
)

# Local imports
from .globals import METADATA_SUBDOMAIN_NAME


def get_metadata_url(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint,
        METADATA_SUBDOMAIN_NAME
    )


def get_metadata_request_response_results(
        endpoint: str,
        params: Dict = None,
):
    return get_request_response_results(get_metadata_url(endpoint), params=params)


def get_item_objs_from_item_id_list(
        item_id_list: List[str],
        item_identifier: str,
        endpoint: str,
        accept_missing=False
) -> List[Dict[str, Any]]:

    # Get query list
    try:
        query_list = get_metadata_request_response_results(
            endpoint,
            {
                item_identifier: item_id_list
            }
        )
    except HTTPError as e:
        raise ValueError(f"Could not get item from item id list {item_id_list} from endpoint {endpoint}") from e

    # Accept missing
    if accept_missing:
        return query_list

    try:
        assert len(query_list) == len(item_id_list)
    except AssertionError:
        # If we don't find all the items, we need to raise an error
        item_ids_response = list(map(
            lambda item_id_response_iter_: item_id_response_iter_[item_identifier],
            query_list
        ))
        missing_items_list = list(set(item_id_list) - set(item_ids_response))
        raise ValueError(f"Some items were not found in the response, {missing_items_list}")
    return query_list


def get_item_from_item_id_list_batched(
        item_id_list: List[str],
        item_identifier: str,
        endpoint: str,
        accept_missing: bool = False,
        batch_size: int = 50
) -> List[Dict[str, Any]]:
    """
    Get items from a list of item ids
    We batch the requests to avoid hitting the API limits
    :param item_id_list:
    :param item_identifier:
    :param endpoint:
    :param accept_missing:
    :param batch_size:
    :return:
    """
    item_id_lists = batched(item_id_list, batch_size)

    # Get the items from the list of item ids
    try:
        return list(reduce(
            concat,
            list(map(
                lambda item_batch_: (
                    get_item_objs_from_item_id_list(
                        item_id_list=item_batch_,
                        item_identifier=item_identifier,
                        endpoint=endpoint,
                        accept_missing=accept_missing
                    )
                ),
                item_id_lists
            ))
        ))
    except TypeError as e:
        # TypeError: reduce() of empty sequence with no initial value
        return []

# Determine all the public classes and functions
# that should be available for import

from .contact_helpers import (
    get_contact_from_contact_id,
    get_contacts_list_from_contact_id_list,
    get_contact_orcabus_id_from_contact_id,
    get_contact_from_contact_orcabus_id,
    get_contacts_list_from_contact_orcabus_id_list,
    coerce_contact_id_or_orcabus_id_to_contact_orcabus_id,
    get_all_contacts,
    list_libraries_for_contact_id,
    list_libraries_for_contact_orcabus_id,
)

from .individual_helpers import (
    get_individual_from_individual_id,
    get_individuals_list_from_individual_id_list,
    get_individual_orcabus_id_from_individual_id,
    get_individual_from_individual_orcabus_id,
    get_individuals_list_from_individual_orcabus_id_list,
    coerce_individual_id_or_orcabus_id_to_individual_orcabus_id,
    get_all_individuals,
    list_libraries_in_individual,
)

from .library_helpers import (
    get_library_from_library_id,
    get_libraries_list_from_library_id_list,
    get_library_orcabus_id_from_library_id,
    get_library_id_from_library_orcabus_id,
    coerce_library_id_or_orcabus_id_to_library_orcabus_id,
    get_library_from_library_orcabus_id,
    get_libraries_from_library_orcabus_id_list,
    get_subject_from_library_id,
    get_library_type,
    get_library_assay_type,
    get_library_phenotype,
    get_library_workflow,
    get_all_libraries,
    get_project_list_from_library_orcabus_id,
    get_project_list_from_library_id,
    get_contact_list_from_library_orcabus_id,
    get_contact_list_from_library_id
)

from .project_helpers import (
    get_project_from_project_id,
    get_projects_list_from_project_id_list,
    get_project_orcabus_id_from_project_id,
    coerce_project_id_or_orcabus_id_to_project_orcabus_id,
    get_project_from_project_orcabus_id,
    get_projects_list_from_project_orcabus_id_list,
    get_all_projects,
    list_libraries_in_project,
)

from .sample_helpers import (
    get_sample_from_sample_id,
    get_samples_list_from_sample_id_list,
    get_sample_orcabus_id_from_sample_id,
    get_sample_from_sample_orcabus_id,
    get_samples_list_from_sample_orcabus_id_list,
    coerce_sample_id_or_orcabus_id_to_sample_orcabus_id,
    list_libraries_in_sample,
    get_all_samples,
)

from .subject_helpers import (
    get_subject_from_subject_id,
    get_subjects_list_from_subject_id_list,
    coerce_subject_id_or_orcabus_id_to_subject_orcabus_id,
    get_subject_orcabus_id_from_subject_id,
    get_subjects_list_from_subject_orcabus_id_list,
    get_subject_from_subject_orcabus_id,
    list_samples_in_subject,
    list_libraries_in_subject,
    get_all_subjects,
)

__all__ = [
    # Contact Helpers
    "get_contact_from_contact_id",
    "get_contacts_list_from_contact_id_list",
    "get_contact_orcabus_id_from_contact_id",
    "get_contact_from_contact_orcabus_id",
    "get_contacts_list_from_contact_orcabus_id_list",
    "coerce_contact_id_or_orcabus_id_to_contact_orcabus_id",
    "get_all_contacts",
    "list_libraries_for_contact_id",
    "list_libraries_for_contact_orcabus_id",

    # Individual Helpers
    "get_individual_from_individual_id",
    "get_individuals_list_from_individual_id_list",
    "get_individual_orcabus_id_from_individual_id",
    "get_individual_from_individual_orcabus_id",
    "get_individuals_list_from_individual_orcabus_id_list",
    "coerce_individual_id_or_orcabus_id_to_individual_orcabus_id",
    "get_all_individuals",
    "list_libraries_in_individual",

    # Library Helpers
    "get_library_from_library_id",
    "get_libraries_list_from_library_id_list",
    "get_library_orcabus_id_from_library_id",
    "get_library_id_from_library_orcabus_id",
    "coerce_library_id_or_orcabus_id_to_library_orcabus_id",
    "get_library_from_library_orcabus_id",
    "get_libraries_from_library_orcabus_id_list",
    "get_subject_from_library_id",
    "get_library_type",
    "get_library_assay_type",
    "get_library_phenotype",
    "get_library_workflow",
    "get_all_libraries",
    "get_project_list_from_library_orcabus_id",
    "get_project_list_from_library_id",
    "get_contact_list_from_library_orcabus_id",
    "get_contact_list_from_library_id",

    # Project Helpers
    "get_project_from_project_id",
    "get_projects_list_from_project_id_list",
    "get_project_orcabus_id_from_project_id",
    "coerce_project_id_or_orcabus_id_to_project_orcabus_id",
    "get_project_from_project_orcabus_id",
    "get_projects_list_from_project_orcabus_id_list",
    "get_all_projects",
    "list_libraries_in_project",

    # Sample Helpers
    "get_sample_from_sample_id",
    "get_samples_list_from_sample_id_list",
    "get_sample_orcabus_id_from_sample_id",
    "get_sample_from_sample_orcabus_id",
    "get_samples_list_from_sample_orcabus_id_list",
    "coerce_sample_id_or_orcabus_id_to_sample_orcabus_id",
    "list_libraries_in_sample",
    "get_all_samples",

    # Subject Helpers
    "get_subject_from_subject_id",
    "get_subjects_list_from_subject_id_list",
    "coerce_subject_id_or_orcabus_id_to_subject_orcabus_id",
    "get_subject_orcabus_id_from_subject_id",
    "get_subjects_list_from_subject_orcabus_id_list",
    "get_subject_from_subject_orcabus_id",
    "list_samples_in_subject",
    "list_libraries_in_subject",
    "get_all_subjects",
]