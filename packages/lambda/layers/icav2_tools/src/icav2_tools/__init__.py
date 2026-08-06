#!/usr/bin/env python
"""ICAv2 tools for managing storage configurations, credentials, and environment variables
for Illumina Connected Analytics v2 integration."""

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

# We also want to set up our environment variables as global variables, so that future calls
# On the same lambda do not need to re-initialize these variables
# While we use the lambda params-and-secrets secret extension, this does not work
# When we need to list params in a path
STORAGE_CONFIGURATION_FILE = None
PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_FILE = None
STORAGE_CREDENTIAL_FILE = None


def create_storage_configuration_file() -> Path:
    """Create a temporary YAML file containing the storage configuration list from SSM parameters.

    Returns:
        Path to the created temporary YAML file.
    """
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


def get_storage_configuration_file() -> Path:
    """Get or create the cached storage configuration file.

    Uses module-level caching to avoid recreating the file on subsequent Lambda
    invocations.

    Returns:
        Path to the storage configuration YAML file.
    """
    global STORAGE_CONFIGURATION_FILE
    if STORAGE_CONFIGURATION_FILE is None:
        STORAGE_CONFIGURATION_FILE = create_storage_configuration_file()
    return STORAGE_CONFIGURATION_FILE


def create_project_to_storage_configuration_mapping_file() -> Path:
    """Create a temporary YAML file containing the project-to-storage-configuration mapping
    from SSM parameters.

    Returns:
        Path to the created temporary YAML file.
    """
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


def get_project_to_storage_configuration_mapping_file() -> Path:
    """Get or create the cached project-to-storage-configuration mapping file.

    Uses module-level caching to avoid recreating the file on subsequent Lambda
    invocations.

    Returns:
        Path to the project-to-storage-configuration YAML file.
    """
    global PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_FILE
    if PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_FILE is None:
        PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_FILE = create_project_to_storage_configuration_mapping_file()
    return PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_FILE


def create_storage_credential_file() -> Path:
    """Create a temporary YAML file containing the storage credential list from SSM parameters.

    Returns:
        Path to the created temporary YAML file.
    """
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


def get_storage_credential_file() -> Path:
    """Get or create the cached storage credential file.

    Uses module-level caching to avoid recreating the file on subsequent Lambda
    invocations.

    Returns:
        Path to the storage credential YAML file.
    """
    global STORAGE_CREDENTIAL_FILE
    if STORAGE_CREDENTIAL_FILE is None:
        STORAGE_CREDENTIAL_FILE = create_storage_credential_file()
    return STORAGE_CREDENTIAL_FILE


def set_icav2_env_vars():
    """
    Set the environment variables for the ICAV2 API
    :return:
    """
    # Standard environment variables
    environ["ICAV2_BASE_URL"] = ICAV2_BASE_URL
    environ["ICAV2_ACCESS_TOKEN"] = get_icav2_access_token()

    # Configuration files needed to map storage configurations
    environ["ICAV2_STORAGE_CONFIGURATION_LIST_FILE"] = str(get_storage_configuration_file())
    environ["ICAV2_PROJECT_TO_STORAGE_CONFIGURATION_MAPPING_LIST_FILE"] = str(get_project_to_storage_configuration_mapping_file())
    environ["ICAV2_STORAGE_CREDENTIAL_LIST_FILE"] = str(get_storage_credential_file())


__all__ = [
    "set_icav2_env_vars"
]
