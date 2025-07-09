# Imports
import re
from typing import Literal

# AWS PARAMETERS
DATA_SHARING_SUBDOMAIN_NAME = "data-sharing"

# API ENDPOINTS
PACKAGE_ENDPOINT = "api/v1/package"
PUSH_ENDPOINT = "api/v1/push"

# REGEX
ORCABUS_ULID_REGEX_MATCH = re.compile(r'^[a-z0-9]{3}\.[A-Z0-9]{26}$')


