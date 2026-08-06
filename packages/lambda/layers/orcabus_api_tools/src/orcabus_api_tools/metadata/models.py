#!/usr/bin/env python3
"""TypedDict models for the OrcaBus metadata service.

Defines the data structures for metadata entities (Library, Sample, Subject,
Individual, Project, Contact) at various detail levels: base, detail, and full.
"""

from typing import (
    TypedDict,
    Optional, List
)


# Base Objects
class MetadataBase(TypedDict):
    """Base metadata object containing only the OrcaBus identifier."""
    orcabusId: str


class LibraryBase(MetadataBase):
    """Base library object with OrcaBus ID and library ID."""

    libraryId: str


class SampleBase(MetadataBase):
    """Base sample object with OrcaBus ID and sample ID."""

    sampleId: str


class SubjectBase(MetadataBase):
    """Base subject object with OrcaBus ID and subject ID."""

    subjectId: str


class IndividualBase(MetadataBase):
    """Base individual object with OrcaBus ID and individual ID."""

    individualId: str


class ProjectBase(MetadataBase):
    """Base project object with OrcaBus ID and project ID."""

    projectId: str


class ContactBase(MetadataBase):
    """Base contact object with OrcaBus ID and contact ID."""

    contactId: str


# Detailed Objects - Often outputs of API calls from other metadata endpoints
class LibraryDetail(LibraryBase):
    """Detailed library object with sequencing metadata fields."""

    phenotype: Optional[str]
    workflow: Optional[str]
    quality: Optional[str]
    type: Optional[str]
    assay: Optional[str]
    coverage: Optional[float]
    overrideCycles: Optional[str]


class SampleDetail(SampleBase):
    """Detailed sample object with external sample ID and source."""

    externalSampleId: Optional[str]
    source: Optional[str]


class SubjectDetail(SubjectBase):
    """Detailed subject object (currently no additional fields)."""

    pass


class IndividualDetail(IndividualBase):
    """Detailed individual object with source information."""

    source: Optional[str]


class ProjectDetail(ProjectBase):
    """Detailed project object with name and description."""

    name: Optional[str]
    description: Optional[str]


class ContactDetail(ContactBase):
    """Detailed contact object with name, email, and description."""

    name: Optional[str]
    email: Optional[str]
    description: Optional[str]


# Add complete objects
# These contain the sets of other metadata objects
class Library(LibraryDetail):
    """Full library object including associated sample, subject, and project sets."""

    sample: Optional[SampleDetail]
    subject: Optional[SubjectDetail]
    projectSet: Optional[List[ProjectDetail]]


class Sample(SampleDetail):
    """Full sample object including its associated library set."""

    librarySet: Optional[List[LibraryDetail]]


class Subject(SubjectDetail):
    """Full subject object including associated library and individual sets."""

    librarySet: Optional[List[LibraryDetail]]
    individualSet: Optional[List[IndividualDetail]]


class Individual(IndividualDetail):
    """Full individual object including its associated subject set."""

    subjectSet: Optional[List[SubjectDetail]]


class Project(ProjectDetail):
    """Full project object including its associated contact set."""

    contactSet: Optional[List[ContactDetail]]


class Contact(ContactDetail):
    """Full contact object including its associated project set."""

    projectSet: Optional[List[ProjectDetail]]


class LimsRow(TypedDict):
    """LIMS-compatible row containing key identifiers for a library in a sequencing run."""

    externalSubjectId: Optional[str]
    externalSampleId: Optional[str]
    individualId: Optional[str]
    sampleId: Optional[str]
    libraryId: Optional[str]
    instrumentRunId: Optional[str]
    projectName: Optional[str]
    sampleType: Optional[str]
    assay: Optional[str]
    phenotype: Optional[str]
