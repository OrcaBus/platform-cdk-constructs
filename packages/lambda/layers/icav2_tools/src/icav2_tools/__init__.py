#!/usr/bin/env python

# Standard imports
from os import environ
from tempfile import NamedTemporaryFile
from ruamel.yaml import YAML
from pathlib import Path

# Local imports
from .aws_helpers import (
    get_icav2_access_token,
    get_storage_configuration_list,
    get_project_to_storage_configuration_list,
    get_storage_credential_list
)
from .globals import ICAV2_BASE_URL


def create_storage_configuration_file() -> Path:
    storage_configuration_file = Path(NamedTemporaryFile(
        delete=False,
        prefix='storage-configuration',
        suffix='.yaml'
    ).name)
    yaml = YAML()
    with open(storage_configuration_file, 'w') as file_h:
        yaml.dump(
            get_storage_configuration_list(),
            file_h
        )
    return storage_configuration_file


def create_project_to_storage_configuration_mapping_file() -> Path:
    project_to_storage_configuration_file = Path(NamedTemporaryFile(
        delete=False,
        prefix='project-to-storage-configuration',
        suffix='.yaml'
    ).name)
    yaml = YAML()
    with open(project_to_storage_configuration_file, 'w') as file_h:
        yaml.dump(
            get_project_to_storage_configuration_list(),
            file_h
        )
    return project_to_storage_configuration_file


def create_storage_credential_file() -> Path:
    storage_credential_file = Path(NamedTemporaryFile(
        delete=False,
        prefix='storage-credential',
        suffix='.yaml'
    ).name)
    yaml = YAML()
    with open(storage_credential_file, 'w') as file_h:
        yaml.dump(
            get_storage_credential_list(),
            file_h
        )
    return storage_credential_file


def set_icav2_env_vars():
    """
    Set the environment variables for the ICAV2 API
    :return:
    """
    # Standard environment variables
    environ["ICAV2_BASE_URL"] = ICAV2_BASE_URL
    environ["ICAV2_ACCESS_TOKEN"] = get_icav2_access_token()

    # Configuration files needed to map storage configurations
    environ["ICAV2_STORAGE_CONFIGURATION_LIST_FILE"] = str(create_storage_configuration_file())
    environ["ICAV2_PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_LIST_FILE"] = str(create_project_to_storage_configuration_mapping_file())
    environ["ICAV2_STORAGE_CREDENTIAL_LIST_FILE"] = str(create_storage_credential_file())


__all__ = [
    "set_icav2_env_vars"
]
