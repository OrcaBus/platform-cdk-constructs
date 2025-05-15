
# Standard imports
import typing
from io import BytesIO
from os import environ
from time import sleep
from typing import Tuple
from urllib.parse import urlparse
import boto3
import pandas as pd

# Local imports
from .globals import DATABASE_ENV_VAR, DATA_SOURCE_ENV_VAR, WORKGROUP_ENV_VAR

if typing.TYPE_CHECKING:
    from mypy_boto3_athena import AthenaClient
    from mypy_boto3_s3 import S3Client


def get_athena_client() -> 'AthenaClient':
    return boto3.client('athena')


def get_s3_client() -> 'S3Client':
    return boto3.client('s3')


def get_bucket_key_tuple_from_s3_uri(s3_uri: str) -> Tuple[str, str]:
    urlobj = urlparse(s3_uri)

    return urlobj.netloc, urlobj.path.lstrip('/')


def run_athena_sql_query(sql_query: str) -> pd.DataFrame:
    from .dataframe_helpers import get_pandas_dtypes_from_athena_query_execution

    athena_query_execution_id = get_athena_client().start_query_execution(
        QueryString=sql_query,
        QueryExecutionContext={
            "Database": environ[DATABASE_ENV_VAR],
            "Catalog": environ[DATA_SOURCE_ENV_VAR]
        },
        WorkGroup=environ[WORKGROUP_ENV_VAR],
    )['QueryExecutionId']

    while True:
        status = get_athena_client().get_query_execution(
            QueryExecutionId=athena_query_execution_id
        )['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

        sleep(5)

    if status in ['FAILED', 'CANCELLED']:
        raise RuntimeError(f"Query failed: {status}")

    # Get the result info
    column_dtypes = get_pandas_dtypes_from_athena_query_execution(
        query_execution_id=athena_query_execution_id
    )

    # Get the results
    result_location = get_athena_client().get_query_execution(
        QueryExecutionId=athena_query_execution_id
    )['QueryExecution']['ResultConfiguration']['OutputLocation']

    bucket, key = get_bucket_key_tuple_from_s3_uri(result_location)

    return pd.read_csv(
        BytesIO(
            get_s3_client().get_object(
                Bucket=bucket,
                Key=key
            )['Body'].read(),
        ),
        dtype=column_dtypes
    )
