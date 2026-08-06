#!/usr/bin/env python3

"""
Mart query module providing Athena SQL query execution and result retrieval.

Exports the primary function for running SQL queries against OrcaBus data marts
and returning results as pandas DataFrames.
"""

# Set __all__
from .aws_helpers import run_athena_sql_query

__all__ = [
    "run_athena_sql_query"
]