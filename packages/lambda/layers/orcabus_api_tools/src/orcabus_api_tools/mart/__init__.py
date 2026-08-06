#!/usr/bin/env python3

"""Mart query module providing Athena SQL query execution against OrcaBus data marts."""

# Set __all__
from .aws_helpers import run_athena_sql_query

__all__ = [
    "run_athena_sql_query"
]