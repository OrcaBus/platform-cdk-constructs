#!/usr/bin/env python3

"""Global constants for the fastq decompression service, including subdomain names and API endpoints."""

import re

# AWS PARAMETERS
FASTQ_DECOMPRESSION_SUBDOMAIN_NAME = "fastq-decompression"

# API ENDPOINTS
JOB_ENDPOINT = "api/v1/jobs"

# REGEX
ORCABUS_ULID_REGEX_MATCH = re.compile(r'^[a-z0-9]{3}\.[A-Z0-9]{26}$')
