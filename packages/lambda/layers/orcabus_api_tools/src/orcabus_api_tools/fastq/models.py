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
    List,
    NotRequired,
    Union,
    Literal
)
from datetime import datetime


FastqJobType = Literal[
    'QC',
    'FILE_COMPRESSION',
    'NTSM',
    'READ_COUNT',
]

# Deprecated: Use FastqJobType instead
JobType = FastqJobType


FastqSetJobType = Literal[
    'RUN_EXTRACT_FINGERPRINT',
]


JobStatus = Literal[
    "PENDING",
    "RUNNING",
    "FAILED",
    "SUCCEEDED",
]



class FileStorageObject(TypedDict):
    """S3 file storage object with ingest and location metadata."""

    s3IngestId: str
    s3Uri: str
    storageClass: str
    sha256: str


class FastqStorageObject(FileStorageObject):
    """FASTQ file storage object with compression size and checksum metadata."""

    gzipCompressionSizeInBytes: int
    rawMd5sum: str


class ReadSet(TypedDict):
    """A pair of FASTQ read files (R1 and R2) with their compression format."""

    r1: FastqStorageObject
    r2: FastqStorageObject
    compressionFormat: str


class Library(TypedDict):
    """Minimal library reference containing OrcaBus ID and library ID."""

    orcabusId: str
    libraryId: str


class SequaliReportsDict(TypedDict):
    """Collection of Sequali QC report file references."""

    sequaliHtml: FileStorageObject
    sequaliParquet: FileStorageObject
    multiqcHtml: FileStorageObject
    multiqcParquet: FileStorageObject


class QcStats(TypedDict):
    """Quality control statistics for a FASTQ file."""

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
    """Deprecated: Use FastqCreate instead. Parameters for creating a FASTQ record."""

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
    """Deprecated: Use Fastq instead. FASTQ record returned from the API."""

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
    """FASTQ record returned from the API, representing a single FASTQ file pair."""

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
    """Parameters for creating a new FASTQ record."""

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
    """Parameters for creating a new FASTQ set."""

    library: Library
    fastqSet: List[Union[str, Fastq]]
    allowAdditionalFastq: bool
    isCurrentFastqSet: bool


class FastqSet(TypedDict):
    """A FASTQ set grouping multiple FASTQ records for a library."""

    id: str
    library: Library
    fastqSet: List[Fastq]
    allowAdditionalFastq: bool
    isCurrentFastqSet: bool
    somalier: Optional[FileStorageObject]

class ReadCount(TypedDict):
    """Read count and estimated base count for a FASTQ file."""

    readCount: int
    baseCountEst: int


class FileCompressionInformation(TypedDict):
    """File compression metadata including format and sizes."""

    compressionFormat: str
    r1GzipCompressionSizeInBytes: Optional[int]
    r2GzipCompressionSizeInBytes: Optional[int]
    r1RawMd5sum: Optional[int]
    r2RawMd5sum: Optional[int]


class FastqListRowDict(TypedDict):
    """FASTQ list row in workflow-compatible dictionary format (for CWL/WDL inputs)."""

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



class FastqJob(TypedDict):
    """A job associated with a FASTQ record (QC, compression, NTSM, read count)."""

    id: str
    fastqId: str
    jobType: FastqJobType
    stepsExecutionArn: str
    status: JobStatus
    startTime: datetime
    endTime: Optional[datetime]


class FastqSetJob(TypedDict):
    """A job associated with a FASTQ set (e.g., fingerprint extraction)."""
    id: str
    fastqSetId: str
    jobType: FastqSetJobType
    stepsExecutionArn: str
    status: JobStatus
    startTime: datetime
    endTime: Optional[datetime]


# Deprecated: Use FastqJob instead
Job = FastqJob

BoolLiteral = Literal[
    'ALL',
    True,
    False
]


class FastqGetResponseParameters(TypedDict):
    """Parameters for controlling FASTQ GET response detail level."""

    includeS3Details: NotRequired[bool]


class StandardQueryParameters(TypedDict):
    """Standard pagination query parameters."""

    page: NotRequired[int]
    rowsPerPage: NotRequired[int]


class MetadataQueryParameter(TypedDict):
    """Single-value metadata query parameters for filtering FASTQs."""

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
    """Instrument run filtering parameters."""

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
    """Deprecated: Use FastqQueryParameters instead. Combined FASTQ query parameters."""

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
    """Combined FASTQ query parameters supporting pagination, metadata, and instrument run filters."""

    valid: NotRequired[BoolLiteral]
    includeS3Details: NotRequired[BoolLiteral]
    fastqSetId: NotRequired[str]


class FastqSetQueryParameters(
    StandardQueryParameters,
    MetadataQueryParameter,
    MetadataQueryParametersList,
    InstrumentRunIdQueryParameters
):
    """Query parameters for listing FASTQ sets with filtering options."""

    currentFastqSet: NotRequired[BoolLiteral]
    allowAdditionalFastq: NotRequired[BoolLiteral]
    includeS3Details: NotRequired[BoolLiteral]

# Additional types
VALID_BATCH_KEYS = Literal[
    'library', 'sample', 'subject',
    'individual', 'project', 'instrumentRunId'
]
