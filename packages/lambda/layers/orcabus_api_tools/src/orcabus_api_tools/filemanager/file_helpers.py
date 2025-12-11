#!/usr/bin/env python3

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
) -> List[FileObject]:

    # Get files from cache
    all_files_list = get_file_manager_request_response_results(S3_ATTRIBUTES_LIST_ENDPOINT, {
        "portalRunId": portal_run_id,
        "currentState": json.dumps(True)
    })

    if not remove_log_files:
        return all_files_list

    return list(filter(
        lambda file_iter_: not (
            f"logs/{portal_run_id}/" in file_iter_['key'] or
            f"cache/{portal_run_id}/" in file_iter_['key']
        ),
        all_files_list
    ))


def list_output_files_from_portal_run_id(
        portal_run_id: str
) -> List[FileObject]:
    return list(filter(
        lambda file_iter_: not (
                f"cache/{portal_run_id}/" in file_iter_['key']
        ),
        list_files_from_portal_run_id(
            portal_run_id=portal_run_id,
            remove_log_files=True
        )
    ))


def get_portal_run_id_root_prefix(portal_run_id: str) -> str:
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
    return get_file_object_from_s3_uri(s3_uri)['s3ObjectId']


def get_s3_uri_from_s3_object_id(s3_object_id: str) -> str:
    file_object: FileObject = get_file_object_from_id(s3_object_id)
    return f"s3://{file_object['bucket']}/{file_object['key']}"


def get_s3_uri_from_ingest_id(
        ingest_id: str,
        bucket: Optional[str] = None,
        key_prefix: Optional[str] = None
) -> str:
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
    """
    Get presigned urls from a list of ingest ids using the bulk presign method
    :param ingest_ids:
    :return:
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
    return boto3.client('sts')


def get_cache_bucket_from_account_id() -> str:
    return S3_BUCKETS_BY_ACCOUNT_ID["cache"][get_sts_client().get_caller_identity()['Account']]

def get_archive_fastq_bucket_from_account_id():
    return S3_BUCKETS_BY_ACCOUNT_ID["archive_fastq"][get_sts_client().get_caller_identity()['Account']]

def get_archive_analysis_bucket_from_account_id():
    return S3_BUCKETS_BY_ACCOUNT_ID["archive_analysis"][get_sts_client().get_caller_identity()['Account']]

def get_restore_prefix_from_account_id():
    return S3_PREFIXES_BY_ACCOUNT_ID["restore"][get_sts_client().get_caller_identity()['Account']]

def get_analysis_cache_prefix_from_account_id():
    return S3_PREFIXES_BY_ACCOUNT_ID["analysis"][get_sts_client().get_caller_identity()['Account']]

def update_ingest_id(s3_object_id: str, new_ingest_id: str) -> Dict:
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
        prefix: str
):
    # We might want to make sure this has completed before moving onto a next step
    # Sync the file manager with the S3 bucket and prefix
    file_manager_post_request(
        endpoint=S3_SYNC_ENDPOINT,
        json_data={
            "bucket": bucket,
            "prefix": f"{prefix.rstrip('/')}/",
        }
    )