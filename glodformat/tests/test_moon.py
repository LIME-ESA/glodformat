"""Tests for moon module"""
import unittest
from importlib.resources import files, as_file

from glodformat.moon import validate_moon_observation


class TestMoon(unittest.TestCase):
    def test_val_moon(self):
        data_file = files("glodformat.tests").joinpath(
            "data/W_XX-EUMETSAT-Darmstadt,VISNIR+SUBSET+MOON,MSG3+SEVIRI_C_EUMG_20140318140112_01.nc"
        )
        with as_file(data_file) as path:
            validate_moon_observation(path, strict=True)


if __name__ == "__main__":
    unittest.main()
