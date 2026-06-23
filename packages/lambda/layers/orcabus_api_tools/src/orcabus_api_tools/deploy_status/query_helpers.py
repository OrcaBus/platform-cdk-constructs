#!/usr/bin/env python3

"""
Query helpers -

get_job_from_job_id

get_unarchiving_job_list

"""

# Type hints
from typing import List, cast

# Shared imports
from utils.requests_helpers import get_request

# Local imports
from . import get_deploy_status_endpoint
from .globals import GET_ALL_STACKS_ENDPOINT
from .models import StackEventResponseDict


def get_all_stacks_summary() -> List[StackEventResponseDict]:
    return cast(List[StackEventResponseDict], get_request(get_deploy_status_endpoint(GET_ALL_STACKS_ENDPOINT)))
