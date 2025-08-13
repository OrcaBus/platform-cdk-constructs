#!/usr/bin/env python3

# Standard imports
import typing
from typing import Optional, List, cast
import boto3
import json
from os import environ
import urllib3
from urllib.parse import urlunparse

# Wrapica imports
from wrapica.storage_configuration import StorageConfigurationObjectModel, ProjectToStorageMappingDictModel
from wrapica.storage_credentials import StorageCredentialMappingModel

# Type hinting
if typing.TYPE_CHECKING:
    from mypy_boto3_secretsmanager import SecretsManagerClient
    from mypy_boto3_ssm import SSMClient
    from mypy_boto3_ssm.type_defs import GetParametersByPathResultTypeDef, ParameterTypeDef

# Set globals
from .globals import (
    STORAGE_CONFIGURATIONS_SSM_PATH,
    STORAGE_CREDENTIALS_SSM_PATH,
    PROJECT_TO_STORAGE_CONFIGURATION_SSM_PATH
)

http = urllib3.PoolManager()

LOCAL_HTTP_CACHE_PORT = 2773
PARAMETER_URL = '/systemsmanager/parameters/get/'
SECRETS_URL = '/secretsmanager/get/'

def retrieve_extension_value(url, query):
    url = str(urlunparse((
        'http',
        f'localhost:{LOCAL_HTTP_CACHE_PORT}',
        url, None,
        "&".join(list(map(
            lambda kv: f"{kv[0]}={kv[1]}",
            query.items()
        ))), None
    )))
    headers = {
        "X-Aws-Parameters-Secrets-Token": environ.get('AWS_SESSION_TOKEN')
    }
    response = http.request("GET", url, headers=headers)
    response = json.loads(response.data)
    return response


def get_ssm_value_from_cache(parameter_name: str) -> Optional[str]:
    try:
        return retrieve_extension_value(
            PARAMETER_URL,
            {
                "name": parameter_name,
            }
        )['Parameter']['Value']
    except Exception as e:
        print("Got an exception while trying to get ssm value from cache")
        print(e)
        return None


def get_ssm_list_from_cache(path: str) -> Optional[List[str]]:
    try:
        return retrieve_extension_value(
            PARAMETER_URL,
            {
                "path": path,
                "recursive": "true",
            }
        )
    except Exception as e:
        print("Got an exception while trying to get ssm list from cache")
        print(e)
        return None


def get_secret_value_from_cache(secret_id: str) -> Optional[str]:
    try:
        return retrieve_extension_value(
            SECRETS_URL,
            {
                "secretId": secret_id,
            }
        )['SecretString']
    except Exception as e:
        print("Got an exception while trying to get secret value from cache")
        print(e)
        return None

def get_secretsmanager_client() -> 'SecretsManagerClient':
    return boto3.client('secretsmanager')


def get_ssm_client() -> 'SSMClient':
    return boto3.client('ssm')


def get_secret_value(secret_id) -> str:
    """
    Collect the secret value
    :param secret_id:
    :return:
    """
    secret_value_cached = get_secret_value_from_cache(secret_id)
    if secret_value_cached is not None:
        return secret_value_cached

    # Get the boto3 response
    get_secret_value_response = get_secretsmanager_client().get_secret_value(SecretId=secret_id)

    return get_secret_value_response['SecretString']


def get_ssm_value(parameter_name) -> str:
    """
    Collect the parameter from SSM
    :param parameter_name:
    :return:
    """
    ssm_parameter_cached = get_ssm_value_from_cache(parameter_name)
    if ssm_parameter_cached is not None:
        return ssm_parameter_cached

    # Get the boto3 response
    get_ssm_parameter_response = get_ssm_client().get_parameter(Name=parameter_name)

    return get_ssm_parameter_response['Parameter']['Value']


def get_ssm_parameters_list_by_path(parameter_path: str) -> List['ParameterTypeDef']:
    """
    We cannot use the cache for this function because we don't know what we're missing
    :param parameter_path:
    :return:
    """

    next_token = None
    ssm_response_list = []

    while True:
        ssm_response: 'GetParametersByPathResultTypeDef' = get_ssm_client().get_parameters_by_path(
            **dict(filter(
                lambda kv_iter_: kv_iter_[1] is not None,
                {
                    "Path": parameter_path,
                    "Recursive": True,
                    "NextToken": next_token,
                    "MaxResults": 10,
                }.items()
            ))
        )
        ssm_response_list.extend(
            ssm_response['Parameters']
        )

        if "NextToken" in ssm_response:
            next_token = ssm_response["NextToken"]
        else:
            break

    return ssm_response_list


def get_icav2_access_token() -> str:
    """
    From the AWS Secrets Manager, retrieve the OrcaBus token.
    :return:
    """
    return get_secret_value(environ.get("ICAV2_ACCESS_TOKEN_SECRET_ID"))


def get_storage_configuration_list() -> List['StorageConfigurationObjectModel']:
    """
    Storage configuration list is a list of storage configurations
    :return:
    """
    # Get the ssm parameter list
    storage_configuration_ssm_parameter_list = get_ssm_parameters_list_by_path(str(STORAGE_CONFIGURATIONS_SSM_PATH) + "/")

    return list(map(
        lambda ssm_parameter_obj_iter: cast(
            StorageConfigurationObjectModel,
            json.loads(ssm_parameter_obj_iter['Value'])
        ),
        storage_configuration_ssm_parameter_list
    ))


def get_project_to_storage_configuration_list() -> List['ProjectToStorageMappingDictModel']:
    # Get the ssm parameter list
    project_to_storage_ssm_parameter_list = get_ssm_parameters_list_by_path(str(PROJECT_TO_STORAGE_CONFIGURATION_SSM_PATH) + "/")

    return list(map(
        lambda ssm_parameter_obj_iter: cast(
            ProjectToStorageMappingDictModel,
            json.loads(ssm_parameter_obj_iter['Value'])
        ),
        project_to_storage_ssm_parameter_list
    ))


def get_storage_credential_list() -> List['StorageCredentialMappingModel']:
    # Get the ssm parameter list
    storage_credential_ssm_parameter_list = get_ssm_parameters_list_by_path(str(STORAGE_CREDENTIALS_SSM_PATH) + "/")

    return list(map(
        lambda ssm_parameter_obj_iter: cast(
            StorageCredentialMappingModel,
            json.loads(ssm_parameter_obj_iter['Value'])
        ),
        storage_credential_ssm_parameter_list
    ))