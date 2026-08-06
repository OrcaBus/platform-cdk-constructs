#!/usr/bin/env python3
"""Helper functions for interacting with the OrcaBus File Manager service.

Provides functions for querying file objects, generating presigned URLs,
resolving S3 URIs, and managing file metadata.
"""

# Standard imports
import json
from functools import reduce
from operator import concat
from pathlib import Path
from typing import List, Dict, Union, Optional, Unpack
import typing
import boto3
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, unquote, urlunparse
from itertools import batched
import re

# Local imports
from .errors import S3FileNotFoundError, S3DuplicateFileCopyError
from .models import FileObject, StorageClassPriority, FileQueryParameters
from ..utils.miscell import get_bucket_key_pair_from_uri
from . import (
    get_file_manager_request_response_results,
    get_file_manager_request,
    file_manager_patch_request, file_manager_post_request
)
from .globals import (
    S3_LIST_ENDPOINT,
    S3_BUCKETS_BY_ACCOUNT_ID,
    S3_PREFIXES_BY_ACCOUNT_ID, S3_ATTRIBUTES_LIST_ENDPOINT, S3_SYNC_ENDPOINT
)

if typing.TYPE_CHECKING:
    from mypy_boto3_sts import STSClient


def get_file_object_from_s3_uri(s3_uri: str) -> FileObject:
    """Retrieve a file object by its S3 URI.

    Args:
        s3_uri: The full S3 URI (s3://bucket/key).

    Returns:
        The FileObject matching the URI.

    Raises:
        S3FileNotFoundError: If no file is found at the URI.
        S3DuplicateFileCopyError: If multiple files match the URI.
    """
    s3_bucket, s3_key = get_bucket_key_pair_from_uri(s3_uri)

    response = get_file_manager_request_response_results(S3_LIST_ENDPOINT, {
        "bucket": s3_bucket,
        "key": s3_key,
        "currentState": 'true'
    })

    if len(response) == 0:
        # Try again with current_state=False
        response = get_file_manager_request_response_results(S3_LIST_ENDPOINT, {
            "bucket": s3_bucket,
            "key": s3_key,
            "currentState": 'false'
        })

    if len(response) == 0:
        raise S3FileNotFoundError(s3_uri=s3_uri)

    # Filter responses with no "s3IngestId" field
    response = list(filter(
        lambda result_iter_: result_iter_.get("ingestId", None) is not None,
        response
    ))

    if len(response) == 0:
        raise S3FileNotFoundError(s3_uri=s3_uri)

    if not len(response) ==  1:
        raise S3DuplicateFileCopyError(s3_uri=s3_uri)

    # Return as a FileObject model
    return FileObject(**response[0])


def get_file_object_from_id(s3_object_id: str) -> FileObject:
    """
    Get file object from the id
    :param s3_object_id:
    :return:
    """
    response = get_file_manager_request_response_results(f"{S3_LIST_ENDPOINT}/{s3_object_id}")

    if len(response) == 0:
        raise S3FileNotFoundError(s3_object_id=s3_object_id)
    elif not len(response) == 1:
        raise S3DuplicateFileCopyError(s3_object_id=s3_object_id)

    # Return as a FileObject model
    return FileObject(**response[0])


def get_file_object_from_ingest_id(
        ingest_id: str,
        **kwargs: Unpack[FileQueryParameters]
) -> FileObject:
    """Retrieve a file object by its ingest ID.

    If multiple copies exist, returns the one with highest storage class priority
    and most recent modification date.

    Args:
        ingest_id: The file ingest identifier.
        **kwargs: Additional FileQueryParameters for filtering.

    Returns:
        The FileObject with the best storage class match.

    Raises:
        S3FileNotFoundError: If no file is found with the ingest ID.
    """
    response = get_file_manager_request_response_results(S3_LIST_ENDPOINT, {
        "ingestId": ingest_id,
        **kwargs
    })

    if len(response) == 0:
        raise S3FileNotFoundError(ingest_id=ingest_id)
    elif len(response) == 1:
        return FileObject(**response[0])

    file_objects_list = list(map(
        lambda file_obj_iter_: FileObject(**file_obj_iter_),
        response
    ))

    # Order by storage class
    file_objects_list.sort(
        key=lambda file_obj_iter_: (
            StorageClassPriority[file_obj_iter_['storageClass']],
            -datetime.fromisoformat(file_obj_iter_['lastModifiedDate']).timestamp()
        )
    )

    # Return as a FileObject model
    return file_objects_list[0]


def list_files_from_portal_run_id(
        portal_run_id: str,
        remove_log_files: bool = True,
        remove_cache_files: bool = True,
) -> List[FileObject]:
    """List file objects associated with a portal run ID.

    Args:
        portal_run_id: The portal run identifier.
        remove_log_files: If True, exclude log files from results.
        remove_cache_files: If True, exclude cache files from results.

    Returns:
        A list of FileObject dictionaries matching the criteria.
    """

    # Get files from cache
    files_list = get_file_manager_request_response_results(S3_ATTRIBUTES_LIST_ENDPOINT, {
        "portalRunId": portal_run_id,
        "currentState": json.dumps(True)
    })

    # Check if we want all files
    if not (remove_log_files or remove_cache_files):
        return files_list

    # Filter out logs
    if remove_log_files:
        logs_re_obj = re.compile(rf"/logs/[\w|-]+/{portal_run_id}/")
        files_list = list(filter(
            lambda file_iter_: not logs_re_obj.search(file_iter_['key']),
            files_list
        ))

    # Filter out cache files
    if remove_cache_files:
        cache_re_obj = re.compile(rf"/cache/[\w|-]+/{portal_run_id}/")
        files_list = list(filter(
            lambda file_iter_: not cache_re_obj.search(file_iter_['key']),
            files_list
        ))

    # Return filtered list
    return files_list


def list_output_files_from_portal_run_id(
        portal_run_id: str
) -> List[FileObject]:
    """List output files for a portal run, excluding logs and cache files.

    Args:
        portal_run_id: The portal run identifier.

    Returns:
        A list of FileObject dictionaries for output files only.
    """
    return list_files_from_portal_run_id(
        portal_run_id=portal_run_id,
        remove_log_files=True,
        remove_cache_files=True,
    )


def get_portal_run_id_root_prefix(portal_run_id: str) -> str:
    """Determine the S3 root prefix for a portal run ID.

    Args:
        portal_run_id: The portal run identifier.

    Returns:
        The S3 URI prefix up to and including the portal run ID.

    Raises:
        ValueError: If no files are found for the portal run ID.
    """
    # Get portal run id midfix from portal_run_id
    all_portal_run_id_files = list_output_files_from_portal_run_id(
        portal_run_id
    )

    # Sort by most recent output
    all_portal_run_id_files.sort(
        key=lambda file_iter_: datetime.fromisoformat(file_iter_['lastModifiedDate']).timestamp(),
        reverse=True
    )

    if len(all_portal_run_id_files) == 0:
        raise ValueError(f"No files found for portal run id {portal_run_id}")

    portal_run_id_analysis_file = all_portal_run_id_files[0]

    # Get root for the portal run id
    parts_list = []
    for idx, part in enumerate(Path(portal_run_id_analysis_file['key']).parts):
        if part == portal_run_id:
            parts_list.append(part)
            break
        else:
            parts_list.append(part)
    return str(urlunparse((
        "s3", portal_run_id_analysis_file['bucket'], str("/".join(parts_list)), None, None, None
    )))


def get_presigned_url(s3_object_id: str) -> str:
    """
    Get presigned url
    :param s3_object_id:
    :return:
    """
    response = get_file_manager_request(f"{S3_LIST_ENDPOINT}/presign/{s3_object_id}")

    return str(response)


def get_s3_object_id_from_s3_uri(s3_uri: str) -> str:
    """Get the File Manager S3 object ID for a given S3 URI.

    Args:
        s3_uri: The full S3 URI.

    Returns:
        The s3ObjectId string.
    """
    return get_file_object_from_s3_uri(s3_uri)['s3ObjectId']


def get_s3_uri_from_s3_object_id(s3_object_id: str) -> str:
    """Resolve an S3 object ID to its full S3 URI.

    Args:
        s3_object_id: The File Manager S3 object ID.

    Returns:
        The full S3 URI (s3://bucket/key).
    """
    file_object: FileObject = get_file_object_from_id(s3_object_id)
    return f"s3://{file_object['bucket']}/{file_object['key']}"


def get_s3_uri_from_ingest_id(
        ingest_id: str,
        bucket: Optional[str] = None,
        key_prefix: Optional[str] = None
) -> str:
    """Resolve an ingest ID to its full S3 URI.

    Args:
        ingest_id: The file ingest identifier.
        bucket: Optional bucket filter.
        key_prefix: Optional key prefix filter.

    Returns:
        The full S3 URI (s3://bucket/key).
    """
    file_object: FileObject = get_file_object_from_ingest_id(
        ingest_id=ingest_id,
        **dict(filter(
            lambda param_iter_: param_iter_[1] is not None,
            {
                "bucket": bucket,
                "key": f"{key_prefix}*" if key_prefix else None
            }.items()
        ))
    )
    return f"s3://{file_object['bucket']}/{file_object['key']}"


def get_ingest_id_from_s3_uri(s3_uri: str) -> str:
    """Get the ingest ID for a given S3 URI.

    Args:
        s3_uri: The full S3 URI.

    Returns:
        The ingest ID string.
    """
    return get_file_object_from_s3_uri(s3_uri)['ingestId']


def get_presigned_url_from_ingest_id(ingest_id: str) -> str:
    """
    Get presigned url from ingest id
    :param ingest_id:
    :return:
    """
    return get_presigned_url(get_file_object_from_ingest_id(ingest_id)['s3ObjectId'])


def create_presigned_url_map(s3_object_iter_: Dict, presigned_url_list: List[str]):
    return {
        "ingestId": s3_object_iter_['ingestId'],
        "presignedUrl": next(filter(
            lambda presigned_url_iter_: unquote(urlparse(presigned_url_iter_).path.lstrip("/")) == s3_object_iter_['fileObject']['key'],
            presigned_url_list
        ))
    }


def get_presigned_urls_from_ingest_ids(ingest_ids: List[str]) -> List[Dict[str, str]]:
    """Generate presigned URLs for a list of ingest IDs using bulk presign.

    Args:
        ingest_ids: List of file ingest identifiers.

    Returns:
        A list of dicts with 'ingestId' and 'presignedUrl' keys.
    """
    # Split by groups of 100
    ingest_id_batches = batched(ingest_ids, 20)

    presigned_url_list: List[str] = list(reduce(
        concat,
        list(map(
            lambda ingest_id_batch_: (
                get_file_manager_request_response_results(S3_LIST_ENDPOINT + "/presign", {
                    "ingestId[]": list(ingest_id_batch_)
                })
            ),
            ingest_id_batches
        )),
        []
    ))

    s3_object_list = get_s3_objs_from_ingest_ids_map(ingest_ids)

    # Map the presigned urls to the s3 objects
    return list(map(
        lambda s3_object_iter_: create_presigned_url_map(s3_object_iter_, presigned_url_list),
        s3_object_list
    ))


def get_presigned_url_expiry(s3_presigned_url: str) -> datetime:
    """
    Given a presigned url, return the expiry
    :param s3_presigned_url:
    :return:
    """
    urlobj = urlparse(s3_presigned_url)

    query_dict = dict(map(
        lambda params_iter_: params_iter_.split("=", 1),
        urlparse(s3_presigned_url).query.split("&"))
    )

    # Take the X-Amz-Date value (in 20250121T013812Z format) and add in the X-Amz-Expires value
    creation_time = datetime.strptime(query_dict['X-Amz-Date'], "%Y%m%dT%H%M%SZ")
    expiry_ext = timedelta(seconds=int(query_dict['X-Amz-Expires']))

    return (creation_time + expiry_ext).astimezone(tz=timezone.utc)


def get_s3_objs_from_ingest_ids_map(
        ingest_ids: List[str], **kwargs
) -> List[Dict[str, Union[FileObject, str]]]:
    """Retrieve file objects for a list of ingest IDs, deduplicating by storage class priority.

    Args:
        ingest_ids: List of file ingest identifiers.
        **kwargs: Additional query parameters.

    Returns:
        A list of dicts with 'ingestId' and 'fileObject' keys.
    """
    # Check if the list is empty
    if len(ingest_ids) == 0:
        return []

    # Split by groups of 100
    ingest_id_batches = batched(ingest_ids, 100)

    # Get the s3 objects
    try:
        s3_objects_by_ingest_id = list(map(
            lambda s3_obj_iter: {
                "ingestId": s3_obj_iter['ingestId'],
                "fileObject": s3_obj_iter
            },
            list(reduce(
                concat,
                list(map(
                    lambda ingest_id_batch_:
                        get_file_manager_request_response_results(S3_LIST_ENDPOINT, {
                            "ingestId[]": list(ingest_id_batch_),
                            **kwargs
                        }),
                    ingest_id_batches
                )),
                []
            ))
        ))
    except TypeError as e:
        # TypeError: reduce() of empty iterable with no initial value
        return []

    # Filter out duplicates, select ranked by storage class
    s3_objects_by_ingest_id_filtered = []
    for ingest_id in ingest_ids:
        s3_objects_match = list(filter(
            lambda s3_object_iter_: s3_object_iter_['ingestId'] == ingest_id,
            s3_objects_by_ingest_id
        ))

        if len(s3_objects_match) == 0:
            continue

        s3_objects_match.sort(
            key=lambda s3_object_iter_: (
                StorageClassPriority[s3_object_iter_['fileObject']['storageClass']],
                -datetime.fromisoformat(s3_object_iter_['fileObject']['lastModifiedDate']).timestamp()
            )
        )

        s3_objects_by_ingest_id_filtered.append(
            s3_objects_match[0]
        )

    return s3_objects_by_ingest_id_filtered


def file_search(bucket: str, key: str) -> List[FileObject]:
    """Search for files matching bucket and key criteria.

    Args:
        bucket: The S3 bucket name.
        key: The S3 key or key pattern.

    Returns:
        A list of FileObject dictionaries matching the search.
    """
    filtered_params = dict(
        filter(
            lambda param_iter_: param_iter_[1] is not None,
            {
                "bucket": bucket,
                "key": key
            }
        )
    )
    response = get_file_manager_request_response_results(
        S3_LIST_ENDPOINT,
        params=filtered_params
    )

    # Return as a list of FileObject models
    return response


def list_files_recursively(bucket: str, key: str) -> List[FileObject]:
    """List all files recursively under a bucket and key prefix.

    Args:
        bucket: The S3 bucket name.
        key: The S3 key prefix (wildcard is appended automatically).

    Returns:
        A list of FileObject dictionaries.
    """
    response = get_file_manager_request_response_results(
        S3_LIST_ENDPOINT,
        {
            "bucket": bucket,
            "key": f"{key}*",  # Append wildcard to key
        }
    )

    # Return as a list of FileObject models
    return response


def get_sts_client() -> 'STSClient':
    """Create and return a boto3 STS client.

    Returns:
        A boto3 STSClient instance.
    """
    return boto3.client('sts')


def get_cache_bucket_from_account_id() -> str:
    """Get the pipeline cache bucket name for the current AWS account.

    Returns:
        The S3 bucket name for the cache.
    """
    return S3_BUCKETS_BY_ACCOUNT_ID["cache"][get_sts_client().get_caller_identity()['Account']]

def get_archive_fastq_bucket_from_account_id():
    """Get the archive FASTQ bucket name for the current AWS account.

    Returns:
        The S3 bucket name for archived FASTQs.
    """
    return S3_BUCKETS_BY_ACCOUNT_ID["archive_fastq"][get_sts_client().get_caller_identity()['Account']]

def get_archive_analysis_bucket_from_account_id():
    """Get the archive analysis bucket name for the current AWS account.

    Returns:
        The S3 bucket name for archived analysis files.
    """
    return S3_BUCKETS_BY_ACCOUNT_ID["archive_analysis"][get_sts_client().get_caller_identity()['Account']]

def get_restore_prefix_from_account_id():
    """Get the S3 prefix for restored files in the current AWS account.

    Returns:
        The S3 key prefix for restored files.
    """
    return S3_PREFIXES_BY_ACCOUNT_ID["restore"][get_sts_client().get_caller_identity()['Account']]

def get_analysis_cache_prefix_from_account_id():
    """Get the S3 prefix for analysis cache in the current AWS account.

    Returns:
        The S3 key prefix for analysis cache files.
    """
    return S3_PREFIXES_BY_ACCOUNT_ID["analysis"][get_sts_client().get_caller_identity()['Account']]

def update_ingest_id(s3_object_id: str, new_ingest_id: str) -> Dict:
    """Update the ingest ID for an S3 object in the File Manager.

    Args:
        s3_object_id: The File Manager S3 object ID.
        new_ingest_id: The new ingest ID to assign.

    Returns:
        The API response dict.
    """
    json_data = {
        'ingestId': [
            {
                'op': 'add',
                'path': '/',
                'value': new_ingest_id,
            },
        ],
    }
    return file_manager_patch_request(
        endpoint=f"{S3_LIST_ENDPOINT}/{s3_object_id}",
        json_data=json_data,
        params = {
            "updateTag": json.dumps(True)
        }
    )


def crawl_filemanager_sync(
        bucket: str,
        prefix: Optional[str] = None
):
    """
    Trigger a filemanager sync for the given bucket and prefix
    :param bucket:
    :param prefix:
    """
    # We might want to make sure this has completed before moving onto a next step
    # Sync the file manager with the S3 bucket and prefix
    file_manager_post_request(
        endpoint=S3_SYNC_ENDPOINT,
        json_data=dict(filter(
            lambda kv_iter_: kv_iter_[1] is not None,
            {
                "bucket": bucket,
                "prefix": (
                    f"{prefix.rstrip('/')}/"
                    if (
                            prefix and
                            prefix != "/"
                    )
                    else None
                ),
            }.items()
        ))
    )
