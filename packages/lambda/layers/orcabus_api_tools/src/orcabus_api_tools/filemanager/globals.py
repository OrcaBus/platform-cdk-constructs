#!/usr/bin/env python

# AWS PARAMETERS
FILEMANAGER_SUBDOMAIN_NAME = "file"

S3_LIST_ENDPOINT = "api/v1/s3"

S3_ATTRIBUTES_LIST_ENDPOINT = "api/v1/s3/attributes"

# TODO: Move to env vars
#
S3_BUCKETS_BY_ACCOUNT_ID = {
    "cache": {
        "843407916570": "pipeline-dev-cache-503977275616-ap-southeast-2",
        "455634345446": "pipeline-stg-cache-503977275616-ap-southeast-2",
        "472057503814": "pipeline-prod-cache-503977275616-ap-southeast-2",
    },
    "archive_fastq": {
        "843407916570": "archive-dev-fastq-503977275616-ap-southeast-2",
        "455634345446": "archive-stg-fastq-503977275616-ap-southeast-2",
        "472057503814": "archive-prod-fastq-503977275616-ap-southeast-2",
    },
    "archive_analysis": {
        "843407916570": "archive-dev-analysis-503977275616-ap-southeast-2",
        "455634345446": "archive-stg-analysis-503977275616-ap-southeast-2",
        "472057503814": "archive-prod-analysis-503977275616-ap-southeast-2",
    }
}

S3_PREFIXES_BY_ACCOUNT_ID = {
    "analysis": {
        "843407916570": "byob-icav2/development/analysis",
        "455634345446": "byob-icav2/staging/analysis",
        "472057503814": "byob-icav2/production/analysis",
    },
    "restore": {
        "843407916570": "byob-icav2/development/restored",
        "455634345446": "byob-icav2/staging/restored",
        "472057503814": "byob-icav2/production/restored",
    },
}

