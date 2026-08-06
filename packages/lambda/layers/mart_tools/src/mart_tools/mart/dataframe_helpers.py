#!/usr/bin/env python3

"""
Collect the mart dataframe but ensuring the correct dtype mappings

We do this by

1. Collecting the ColumnInfo from the query results.
2. Mapping the 'label' to the 'type'
3. Then reading the csv from s3, using the dtype mapping coercions

"""

from .models import ATHENA_TO_DTYPES_MAPPING

def get_pandas_dtypes_from_athena_query_execution(query_execution_id):
    """Retrieve column dtype mapping from an Athena query execution.

    Queries the Athena result metadata to determine column types, then maps
    each column to the appropriate pandas dtype for proper type coercion.

    Args:
        query_execution_id: The Athena query execution ID to retrieve metadata for.

    Returns:
        A dictionary mapping column names to their pandas dtype strings.
    """
    from .aws_helpers import get_athena_client

    column_info_dict = get_athena_client().get_query_results(
        QueryExecutionId=query_execution_id
    )['ResultSet']['ResultSetMetadata']['ColumnInfo']

    # Create a dictionary mapping the column name to its type
    return dict(map(
        lambda x: (x['Name'], ATHENA_TO_DTYPES_MAPPING.get(x['Type'])),
        column_info_dict
    ))


