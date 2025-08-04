#!/usr/bin/env python3

"""
{
  "id": "fqr.01JJY7P1AVFGHGVMEDE8T4VWJG",
  "rgid": "ATCCACTG+ACGCACCT.2",
  "index": "ATCCACTG",
  "index2": "ACGCACCT",
  "lane": 2,
  "instrumentRunId": "230223_A00130_0244_AHN3W3DSX5",
  "library": {
    "orcabusId": "lib.01JBMVFP45C2EZRVK67P8JY1D2",
    "libraryId": "L2300223"
  },
  "readSet": {
    "r1": {
      "s3IngestId": "019387bd-2494-7c00-9e41-03e8b6a73306",
      "gzipCompressionSizeInBytes": 49532847794,
      "rawMd5sum": "19e339fdb3c42f0133f5f3b1f9d188e0",  // pragma: allowlist secret
      "s3Uri": "s3://archive-prod-fastq-503977275616-ap-southeast-2/v1/year=2023/month=02/230223_A00130_0244_AHN3W3DSX5/202411226f4f7af0/WGS_TsqNano/MDX230039_L2300223_S7_L002_R1_001.fastq.ora"
    },
    "r2": {
      "s3IngestId": "019387bd-9177-79c1-a489-d940ecc11b11",
      "gzipCompressionSizeInBytes": 53189277581,
      "rawMd5sum": "e857de35a8ca008589d24b2e0f647cc7", // pragma: allowlist secret
      "s3Uri": "s3://archive-prod-fastq-503977275616-ap-southeast-2/v1/year=2023/month=02/230223_A00130_0244_AHN3W3DSX5/202411226f4f7af0/WGS_TsqNano/MDX230039_L2300223_S7_L002_R2_001.fastq.ora"
    },
    "compressionFormat": "ORA"
  },
  "qc": null,
  "readCount": null,
  "baseCountEst": null,
  "isValid": true,
  "ntsm": null
}
"""

from typing import (
    TypedDict,
    Optional,
    Dict,
    List, NotRequired, Union,
    Literal
)
from datetime import datetime


JobType = Literal[
    'QC',
    'FILE_COMPRESSION',
    'NTSM',
    'READ_COUNT',
]


JobStatus = Literal[
    "PENDING",
    "RUNNING",
    "FAILED",
    "SUCCEEDED",
]



class FileStorageObject(TypedDict):
    s3IngestId: str
    s3Uri: str
    storageClass: str
    sha256: str


class FastqStorageObject(FileStorageObject):
    gzipCompressionSizeInBytes: int
    rawMd5sum: str


class ReadSet(TypedDict):
    r1: FastqStorageObject
    r2: FastqStorageObject
    compressionFormat: str


class Library(TypedDict):
    orcabusId: str
    libraryId: str


class SequaliReportsDict(TypedDict):
    sequaliHtml: FileStorageObject
    sequaliParquet: FileStorageObject
    multiqcHtml: FileStorageObject
    multiqcParquet: FileStorageObject


class QcStats(TypedDict):
    insertSizeEstimate: int
    rawWgsCoverageEstimate: int
    r1Q20Fraction: float
    r2Q20Fraction: float
    r1GcFraction: float
    r2GcFraction: float
    duplicationFractionEstimate: float
    sequaliReports: Optional[SequaliReportsDict]


# Deprecated: Use FastqCreate instead
class FastqListRowCreate(TypedDict):
    fastqSetId: Optional[str]
    index: str
    lane: int
    instrumentRunId: str
    library: Library
    platform: Optional[str]
    center: Optional[str]
    date: Optional[datetime]
    readSet: Optional[ReadSet]
    qc: Optional[Dict]
    readCount: Optional[int]
    baseCountEst: Optional[int]
    isValid: Optional[bool]
    ntsm: Optional[FileStorageObject]


# Deprecated: Use Fastq instead
class FastqListRow(TypedDict):
    id: str
    fastqSetId: Optional[str]
    index: str
    lane: int
    instrumentRunId: str
    library: Library
    platform: Optional[str]
    center: Optional[str]
    date: Optional[datetime]
    readSet: Optional[ReadSet]
    qc: Optional[Dict]
    readCount: Optional[int]
    baseCountEst: Optional[int]
    isValid: Optional[bool]
    ntsm: Optional[FileStorageObject]


class Fastq(TypedDict):
    id: str
    fastqSetId: Optional[str]
    index: str
    lane: int
    instrumentRunId: str
    library: Library
    platform: Optional[str]
    center: Optional[str]
    date: Optional[datetime]
    readSet: Optional[ReadSet]
    qc: Optional[QcStats]
    readCount: Optional[int]
    baseCountEst: Optional[int]
    isValid: Optional[bool]
    ntsm: Optional[FileStorageObject]


class FastqCreate(TypedDict):
    fastqSetId: Optional[str]
    index: str
    lane: int
    instrumentRunId: str
    library: Library
    platform: Optional[str]
    center: Optional[str]
    date: Optional[datetime]
    readSet: Optional[ReadSet]
    qc: Optional[QcStats]
    readCount: Optional[int]
    baseCountEst: Optional[int]
    isValid: Optional[bool]
    ntsm: Optional[FileStorageObject]


class FastqSetCreate(TypedDict):
    library: Library
    fastqSet: List[Union[str, Fastq]]
    allowAdditionalFastq: bool
    isCurrentFastqSet: bool


class FastqSet(TypedDict):
    id: str
    library: Library
    fastqSet: List[Fastq]
    allowAdditionalFastq: bool
    isCurrentFastqSet: bool


class ReadCount(TypedDict):
    readCount: int
    baseCountEst: int


class FileCompressionInformation(TypedDict):
    compressionFormat: str
    r1GzipCompressionSizeInBytes: Optional[int]
    r2GzipCompressionSizeInBytes: Optional[int]
    r1RawMd5sum: Optional[int]
    r2RawMd5sum: Optional[int]


class FastqListRowDict(TypedDict):
    rgid: str
    rglb: str
    rgsm: str
    lane: int
    rgcn: str
    rgds: str
    rgdt: str
    rgpl: str
    read1FileUri: str
    read2FileUri: str



class Job(TypedDict):
    id: str
    fastqId: str
    jobType: JobType
    stepsExecutionArn: str
    status: JobStatus
    startTime: datetime
    endTime: Optional[datetime]

BoolLiteral = Literal[
    'ALL',
    True,
    False
]


class FastqGetResponseParameters(TypedDict):
    includeS3Details: NotRequired[bool]


class StandardQueryParameters(TypedDict):
    page: NotRequired[int]
    rowsPerPage: NotRequired[int]


class MetadataQueryParameter(TypedDict):
    library: NotRequired[str]
    sample: NotRequired[str]
    subject: NotRequired[str]
    individual: NotRequired[str]
    project: NotRequired[str]


MetadataQueryParametersList = TypedDict(
    'MetadataQueryParametersList',
    {
        'library[]': NotRequired[List[str]],
        'sample[]': NotRequired[List[str]],
        'subject[]': NotRequired[List[str]],
        'individual[]': NotRequired[List[str]],
        'project[]': NotRequired[List[str]],
    }
)

class InstrumentRunIdQueryParameters(TypedDict):
    index: NotRequired[str]
    lane: NotRequired[int]
    instrumentRunId: NotRequired[str]

InstrumentRunIdQueryParametersList = TypedDict(
    'InstrumentRunIdQueryParametersList',
    {
        'instrumentRunId[]': NotRequired[List[str]],
    }
)


# Deprecated: Use FastqQueryParameters instead
class FastqParameters(
    StandardQueryParameters,
    MetadataQueryParameter,
    InstrumentRunIdQueryParameters,
    MetadataQueryParametersList,
    InstrumentRunIdQueryParametersList
):
    valid: NotRequired[BoolLiteral]
    includeS3Details: NotRequired[BoolLiteral]
    fastqSetId: NotRequired[str]


class FastqQueryParameters(
    StandardQueryParameters,
    MetadataQueryParameter,
    InstrumentRunIdQueryParameters,
    MetadataQueryParametersList,
    InstrumentRunIdQueryParametersList
):
    valid: NotRequired[BoolLiteral]
    includeS3Details: NotRequired[BoolLiteral]
    fastqSetId: NotRequired[str]


class FastqSetQueryParameters(
    StandardQueryParameters,
    MetadataQueryParameter,
    MetadataQueryParametersList,
    InstrumentRunIdQueryParameters
):
    currentFastqSet: NotRequired[BoolLiteral]
    allowAdditionalFastq: NotRequired[BoolLiteral]
    includeS3Details: NotRequired[BoolLiteral]

# Additional types
VALID_BATCH_KEYS = Literal[
    'library', 'sample', 'subject',
    'individual', 'project', 'instrumentRunId'
]
