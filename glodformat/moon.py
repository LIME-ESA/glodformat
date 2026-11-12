"""
This module contains the functionality that validates moon observations files.

It exports the following functions:
    * validate_moon_observation - Validates that a xarray dataset follows the Moon Observation schema.
"""
from typing import Union
import re
from pathlib import Path

import numpy as np
import xarray as xr
import pandera.xarray as pa

from glodformat.netcdfcommon import (
    validate_schema,
    get_valid_metric_units,
    check_stringy,
    check_floating,
    _as_ctx,
)

_check_shape_1 = pa.Check(
    lambda da: da.size == 1, error="Coordinate 'date' must have exactly one element."
)

_UNITS_REGEX = "^(?:" + "|".join(re.escape(v) for v in get_valid_metric_units()) + ")$"

_LUNAR_OBS_SCHEMA = pa.DatasetSchema(
    data_vars={
        "channel_name": pa.DataArraySchema(checks=check_stringy, dims=["chan"]),
        "sat_pos": pa.DataArraySchema(
            checks=check_floating,
            shape=(3,),
            dims=["sat_xyz"],
            attrs={"units": _UNITS_REGEX},
        ),
        "sat_pos_ref": pa.DataArraySchema(checks=check_stringy, dims=[]),
        "irr_obs": pa.DataArraySchema(
            checks=check_floating, dims=["chan"], nullable=True
        ),
    },
    coords={"date": pa.Coordinate(np.datetime64, checks=_check_shape_1)},
    attrs={"data_source": lambda _: True},
)

_LUNAR_OBS_OTHER_SCHEMAS = [
    pa.DatasetSchema(
        data_vars={
            "channel_name": pa.DataArraySchema(checks=check_stringy, dims=["chan"]),
            "sat_pos": pa.DataArraySchema(
                checks=check_floating,
                shape=(3,),
                dims=["sat_xyz"],
                attrs={"units": _UNITS_REGEX},
            ),
            "sat_pos_ref": pa.DataArraySchema(checks=check_stringy, dims=[]),
            "irr_obs": pa.DataArraySchema(
                checks=check_floating, dims=["chan"], nullable=True
            ),
        },
        coords={"date": pa.Coordinate(checks=[check_floating, _check_shape_1])},
        attrs={"data_source": lambda _: True},
    ),
    pa.DatasetSchema(
        data_vars={
            "channel_name": pa.DataArraySchema(checks=check_stringy, dims=["chan"]),
            "sat_pos": pa.DataArraySchema(
                checks=check_floating,
                shape=(3,),
                dims=["sat_xyz"],
                attrs={"units": _UNITS_REGEX},
            ),
            "sat_pos_ref": pa.DataArraySchema(checks=check_stringy, dims=[]),
            "irr_obs": pa.DataArraySchema(
                checks=check_floating, dims=["chan"], nullable=True
            ),
            "date": pa.DataArraySchema(np.datetime64, shape=(1,)),
        },
        attrs={"data_source": lambda _: True},
    ),
    pa.DatasetSchema(
        data_vars={
            "channel_name": pa.DataArraySchema(checks=check_stringy, dims=["chan"]),
            "sat_pos": pa.DataArraySchema(
                checks=check_floating,
                shape=(3,),
                dims=["sat_xyz"],
                attrs={"units": _UNITS_REGEX},
            ),
            "sat_pos_ref": pa.DataArraySchema(checks=check_stringy, dims=[]),
            "irr_obs": pa.DataArraySchema(
                checks=check_floating, dims=["chan"], nullable=True
            ),
            "date": pa.DataArraySchema(checks=check_floating, shape=(1,)),
        },
        attrs={"data_source": lambda _: True},
    ),
]


def _validate_schema_moon_observation(ds: xr.Dataset, strict: bool = False):
    """Validates that a xarray dataset follows the Basic Moon Observation schema.

    The dataset structure is:

    coordinates: 'date': datetime
    dims without coordinates: 'chan' and 'sat_xyz'
    data_vars: 'channel_name': str, 'sat_pos': float, 'sat_pos_ref': str, 'irr_obs': float

    Parameters
    ----------
    ds: xr.Dataset
        Dataset to validate
    strict: bool
        Flag to specify if the check must be exact to the desired schema, or if
        it can pass if it would work in most cases.
    """
    schema = _LUNAR_OBS_SCHEMA
    if strict:
        validate_schema(schema, ds)
    else:
        validate_schema(schema, ds, _LUNAR_OBS_OTHER_SCHEMAS)


def validate_moon_observation(
    data: Union[xr.Dataset, str, Path], strict: bool = False
) -> None:
    """Validates that a dataset follows the Moon Observation schema.

    Parameters
    ----------
    data : xr.Dataset or str or pathlib.Path
        Dataset to validate, or path to a NetCDF file that will be opened
        and validated. If a path is given, the file is opened in read-only
        mode and closed before returning.
    strict : bool
        Flag to specify if the check must be exact to the desired schema, or
        if it can pass if it would work in most cases.

    Raises
    ------
    TypeError
        If ``data`` is neither an ``xr.Dataset``, ``str`` nor ``Path``.
    ValueError
        If the dataset does not conform to any of the accepted SRF schemas.
    """
    with _as_ctx(data) as ds:
        _validate_schema_moon_observation(ds, strict=strict)
