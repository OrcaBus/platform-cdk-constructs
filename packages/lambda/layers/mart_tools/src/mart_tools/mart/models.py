#!/usr/bin/env python

"""
Data type models for Athena-to-Pandas type mapping.

Provides enumerations for Athena DML data types and their corresponding
pandas dtype equivalents, plus a mapping dictionary for type coercion
when reading Athena query results into DataFrames.
"""

from enum import Enum


class AthenaDMLTypes(Enum):
    """Enumeration of Athena DML data types as defined in the AWS documentation."""
    # https://docs.aws.amazon.com/athena/latest/ug/data-types.html
    BOOLEAN = 'boolean'
    TINYINT = 'tinyint'
    SMALLINT = 'smallint'
    INT = 'int'
    INTEGER = 'integer'
    BIGINT = 'bigint'
    REAL = 'real'
    DOUBLE = 'double'
    DECIMAL = 'decimal'
    CHAR = 'char'
    VARCHAR = 'varchar'
    VARBINARY = 'varbinary'
    TIME = 'time'
    TIME_WITH_TIME_ZONE = 'time with time zone'
    TIMESTAMP = 'timestamp'
    TIMESTAMP_WITH_TIME_ZONE = 'timestamp with time zone'
    ARRAY = 'array'
    MAP = 'map'
    ROW = 'row'
    JSON = 'json'
    UUID = 'uuid'
    IPADDRESS = 'ipaddress'


class PandasDtypes(Enum):
    """Enumeration of pandas dtype strings used for Athena result type coercion."""
    # https://numpy.org/doc/stable/reference/arrays.dtypes.html

    # https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#dtypes
    DATETIME_NO_TZ = 'datetime64[ns]'
    DATETIME_TZ_AWARE = 'datetime64[ns, UTC]'
    CATEGORICAL = 'category'
    PERIOD = 'period[<freq>]'
    SPARSE = 'Sparse'
    INTERVAL = 'interval'
    NULLABLE_INTEGER = 'Int64'
    NULLABLE_FLOAT = 'Float64'
    STRINGS = 'string'
    BOOLEAN = 'boolean'
    OBJECT = 'object'


ATHENA_TO_DTYPES_MAPPING = {
    AthenaDMLTypes.BOOLEAN.value: PandasDtypes.BOOLEAN.value,
    AthenaDMLTypes.TINYINT.value: PandasDtypes.NULLABLE_INTEGER.value,
    AthenaDMLTypes.SMALLINT.value: PandasDtypes.NULLABLE_INTEGER.value,
    AthenaDMLTypes.INT.value: PandasDtypes.NULLABLE_INTEGER.value,
    AthenaDMLTypes.INTEGER.value: PandasDtypes.NULLABLE_INTEGER.value,
    AthenaDMLTypes.BIGINT.value: PandasDtypes.NULLABLE_INTEGER.value,
    AthenaDMLTypes.REAL.value: PandasDtypes.NULLABLE_FLOAT.value,
    AthenaDMLTypes.DOUBLE.value: PandasDtypes.NULLABLE_FLOAT.value,
    AthenaDMLTypes.DECIMAL.value: PandasDtypes.NULLABLE_FLOAT.value,
    AthenaDMLTypes.CHAR.value: PandasDtypes.STRINGS.value,
    AthenaDMLTypes.VARCHAR.value: PandasDtypes.STRINGS.value,
    AthenaDMLTypes.VARBINARY.value: PandasDtypes.STRINGS.value,
    AthenaDMLTypes.TIMESTAMP.value: PandasDtypes.DATETIME_NO_TZ.value,
    AthenaDMLTypes.TIMESTAMP_WITH_TIME_ZONE.value: PandasDtypes.DATETIME_TZ_AWARE.value,
    AthenaDMLTypes.ARRAY.value: PandasDtypes.OBJECT.value,
    AthenaDMLTypes.MAP.value: PandasDtypes.OBJECT.value,
    AthenaDMLTypes.ROW.value: PandasDtypes.OBJECT.value,
    AthenaDMLTypes.JSON.value: PandasDtypes.OBJECT.value,
    AthenaDMLTypes.UUID.value: PandasDtypes.STRINGS.value,
    AthenaDMLTypes.IPADDRESS.value: PandasDtypes.STRINGS.value,
}
