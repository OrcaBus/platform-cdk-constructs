# Standard
from typing import Dict, Optional

# Locals
from .globals import FILEMANAGER_SUBDOMAIN_NAME
from ..utils.requests_helpers import get_request_response_results, get_url, get_request, patch_request


def get_file_manager_url(endpoint: str) -> str:
    """
    Get trhe URL for the File Manager endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint=endpoint,
        subdomain=FILEMANAGER_SUBDOMAIN_NAME,
    )


def get_file_manager_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
        return get_request_response_results(
            url=get_file_manager_url(endpoint),
            params=params
        )


def get_file_manager_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(
        get_file_manager_url(endpoint),
        params=params
    )


def file_manager_patch_request(
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None
):
    return patch_request(
        get_file_manager_url(endpoint),
        json_data=json_data,
        params=params
    )


# Set all
from .file_helpers import (
    get_file_object_from_s3_uri,
    get_file_object_from_id,
    get_file_object_from_ingest_id,
    list_files_from_portal_run_id,
    get_presigned_url,
    get_s3_object_id_from_s3_uri,
    get_s3_uri_from_s3_object_id,
    get_s3_uri_from_ingest_id,
    get_ingest_id_from_s3_uri,
    get_presigned_url_from_ingest_id,
    get_presigned_urls_from_ingest_ids,
    get_presigned_url_expiry,
    get_s3_objs_from_ingest_ids_map,
    file_search,
    list_files_recursively,
    get_cache_bucket_from_account_id,
    get_archive_fastq_bucket_from_account_id,
    get_archive_analysis_bucket_from_account_id,
    get_restore_prefix_from_account_id,
    get_analysis_cache_prefix_from_account_id,
    update_ingest_id,
)

__all__ = [
    "get_file_object_from_s3_uri",
    "get_file_object_from_id",
    "get_file_object_from_ingest_id",
    "list_files_from_portal_run_id",
    "get_presigned_url",
    "get_s3_object_id_from_s3_uri",
    "get_s3_uri_from_s3_object_id",
    "get_s3_uri_from_ingest_id",
    "get_ingest_id_from_s3_uri",
    "get_presigned_url_from_ingest_id",
    "get_presigned_urls_from_ingest_ids",
    "get_presigned_url_expiry",
    "get_s3_objs_from_ingest_ids_map",
    "file_search",
    "list_files_recursively",
    "get_cache_bucket_from_account_id",
    "get_archive_fastq_bucket_from_account_id",
    "get_archive_analysis_bucket_from_account_id",
    "get_restore_prefix_from_account_id",
    "get_analysis_cache_prefix_from_account_id",
    "update_ingest_id",
]