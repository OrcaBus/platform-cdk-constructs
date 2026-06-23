#!/usr/bin/env python3

"""
DeployStatus Manager models
"""
# Standard imports
from datetime import datetime
from typing import Literal, TypedDict, NotRequired, Union

# Cloud Formation Constants
# From https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/view-stack-events.html#cfn-console-view-stack-data-resources-status-codes
CloudFormationStackStatusType = Literal[
    'CREATE_COMPLETE',
    'CREATE_IN_PROGRESS',
    'CREATE_FAILED',
    'DELETE_COMPLETE',
    'DELETE_FAILED',
    'DELETE_IN_PROGRESS',
    'REVIEW_IN_PROGRESS',
    'ROLLBACK_COMPLETE',
    'ROLLBACK_FAILED',
    'ROLLBACK_IN_PROGRESS',
    'UPDATE_COMPLETE',
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_FAILED',
    'UPDATE_IN_PROGRESS',
    'UPDATE_ROLLBACK_COMPLETE',
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_ROLLBACK_FAILED',
    'UPDATE_ROLLBACK_IN_PROGRESS',
    'IMPORT_IN_PROGRESS',
    'IMPORT_COMPLETE',
    'IMPORT_ROLLBACK_IN_PROGRESS',
    'IMPORT_ROLLBACK_FAILED',
    'IMPORT_ROLLBACK_COMPLETE',
]

CloudFormationStackStatusWithCfnOutputType = Literal[
    'CREATE_COMPLETE',
    'ROLLBACK_COMPLETE',
    'ROLLBACK_FAILED',
    'UPDATE_COMPLETE',
    'UPDATE_FAILED',
    'UPDATE_ROLLBACK_COMPLETE',
    'IMPORT_COMPLETE',
    'IMPORT_ROLLBACK_FAILED',
    'IMPORT_ROLLBACK_COMPLETE',
]

CloudFormationStackStatusWithoutCfnOutputType = Literal[
    'CREATE_IN_PROGRESS',
    'CREATE_FAILED',
    'DELETE_COMPLETE',
    'DELETE_FAILED',
    'DELETE_IN_PROGRESS',
    'REVIEW_IN_PROGRESS',
    'ROLLBACK_IN_PROGRESS',
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_IN_PROGRESS',
    'UPDATE_ROLLBACK_IN_PROGRESS',
    'IMPORT_IN_PROGRESS',
    'IMPORT_ROLLBACK_IN_PROGRESS',
]


class StackEventResponseWithCfnOutputDict(TypedDict):
    stackOrcabusId: str
    stackId: str
    stackName: str
    eventOrcabusId: str
    eventId: str
    status: CloudFormationStackStatusWithCfnOutputType
    modificationTimestamp: datetime
    gitCommitId: NotRequired[str]


class StackEventResponseWithoutCfnOutputDict(TypedDict):
    stackOrcabusId: str
    stackId: str
    stackName: str
    eventOrcabusId: str
    eventId: str
    status: CloudFormationStackStatusWithoutCfnOutputType
    modificationTimestamp: datetime


StackEventResponseDict = Union[StackEventResponseWithCfnOutputDict, StackEventResponseWithoutCfnOutputDict]
