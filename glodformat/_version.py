"""
glodformat Version Handler Module

Handles versioning for the `glodformat` package.
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("glodformat")
except PackageNotFoundError:
    __version__ = "0.0.0"
