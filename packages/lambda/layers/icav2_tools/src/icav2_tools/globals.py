from pathlib import Path

# Set ICAV2 Base url
ICAV2_BASE_URL = "https://ica.illumina.com/ica/rest"

# Tenant name
TENANT_NAME = "umccr-prod"

# SSM Parameter paths
SSM_PATH_ROOT = Path("/icav2") / TENANT_NAME

# SSM paths for various configurations
STORAGE_CONFIGURATIONS_SSM_PATH = SSM_PATH_ROOT / "storage-configurations"
PROJECT_TO_STORAGE_CONFIGURATION_SSM_PATH = SSM_PATH_ROOT / "project-to-storage-configurations"
STORAGE_CREDENTIALS_SSM_PATH = SSM_PATH_ROOT / "storage-credentials"
