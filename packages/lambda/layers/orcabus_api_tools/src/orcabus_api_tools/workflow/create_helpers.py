from datetime import datetime, timezone
import random

from orcabus_api_tools.workflow.globals import WORKFLOW_RUN_PREFIX


def generate_rand_hex_string(length: int = 8) -> str:
    """
    Generate a random hexadecimal string of a given length.
    :param length: Length of the hexadecimal string to generate.
    :return: Random hexadecimal string.
    """
    return ''.join(random.choices('0123456789abcdef', k=length))


def create_portal_run_id():
    return datetime.now(timezone.utc).strftime("%Y%m%d") + str(generate_rand_hex_string())[0:8]


def create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id(
        workflow_name: str,
        workflow_version: str,
        portal_run_id: str
):
    return '--'.join([
        WORKFLOW_RUN_PREFIX,
        workflow_name.lower(),
        workflow_version.replace(".", "-"),
        portal_run_id
    ])