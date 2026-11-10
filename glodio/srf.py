"""
This module contains the functionality that validates Spectral Response Function files
from GLOD format files.

It exports the following functions:
    * validate_srf: Validates that a xarray dataset follows the SRF schema.
"""
from typing import Union
from pathlib import Path
import re

import numpy as np
import xarray as xr
import pandera.xarray as pa

from glodio.netcdfcommon import (
    validate_schema,
    get_valid_metric_units,
)

_UNITS_REGEX = "^(?:" + "|".join(re.escape(v) for v in get_valid_metric_units()) + ")$"

_SRF_SCHEMA = pa.DatasetSchema(
    data_vars={ # TODO check if None works in pandera
        "srf": pa.DataArraySchema(np.floating, dims=[None, "channel"]),
        "wavelength": pa.DataArraySchema(np.floating, dims=[None, "channel"], attrs={"units": _UNITS_REGEX}),
        "channel_id": pa.DataArraySchema(np.character), # TODO check if works
    },
    coords={"channel": pa.DataArraySchema(np.floating)},
)

_SRF_OTHER_SCHEMAS = [
    pa.DatasetSchema(
        data_vars={
            "srf": pa.DataArraySchema(np.floating, dims=[None, "channel"]),
            "wavelength": pa.DataArraySchema(np.floating, dims=[None, "channel"], attrs={"units": _UNITS_REGEX}),
        },
        coords={
            "channel": pa.DataArraySchema(np.floating),
            "channel_id": pa.DataArraySchema(np.character),
        },
    ),
    pa.DatasetSchema(
        data_vars={
            "srf": pa.DataArraySchema(np.floating, dims=[None, None]),
            "wavelength": pa.DataArraySchema(np.floating, dims=[None, None], attrs={"units": _UNITS_REGEX}),
            "channel": pa.DataArraySchema(np.floating),
            "channel_id": pa.DataArraySchema(np.character),
        },
    ),
    pa.DatasetSchema(
        data_vars={
            "srf": pa.DataArraySchema(np.floating, dims=[None, "wavelength"]),
            "channel_id": pa.DataArraySchema(np.character),
        },
        coords={
            "channel": pa.DataArraySchema(np.floating),
            "wavelength": pa.DataArraySchema(np.floating, attrs={"units": _UNITS_REGEX}),
        },
    ),
]


def _validate_schema_srf(ds: xr.Dataset, strict: bool = False):
    """Validates that a xarray dataset follows the SRF schema.

    The dataset structure is:

    coordinates: 'channel': float
    dims without coordinates: Any name, for example 'sample'.
    data_vars: 'srf': float, 'wavelength': float, 'channel_id': str

    Parameters
    ----------
    ds: xr.Dataset
        Dataset to validate
    strict: bool
        Flag to specify if the check must be exact to the desired schema, or if
        it can pass if it would work in most cases.
    """
    schema = _SRF_SCHEMA
    if strict:
        validate_schema(schema, ds)
    else:
        validate_schema(schema, ds, _SRF_OTHER_SCHEMAS)

def validate_srf(data: Union[xr.Dataset, str, Path], strict: bool = False) -> None:
    """Validates that a dataset follows the SRF schema.

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
    if isinstance(data, (str, Path)):
        with xr.open_dataset(data) as ds:
            _validate_schema_srf(ds, strict=strict)
    elif isinstance(data, xr.Dataset):
        _validate_schema_srf(data, strict=strict)
    else:
        raise TypeError(
            f"validate_srf expected xr.Dataset, str or Path, "
            f"got {type(data).__name__}"
        )
