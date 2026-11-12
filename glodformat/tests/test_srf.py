import unittest
from importlib.resources import files, as_file

from glodformat.srf import validate_srf, validate_srf_for_obs


class TestSRF(unittest.TestCase):
    def test_val_srf(self):
        data_file = files("glodformat.tests").joinpath(
            "data/W_XX-EUMETSAT-Darmstadt_VIS+IR+SRF_MSG3+SEVIRI_C_EUMG.nc"
        )
        with as_file(data_file) as path:
            validate_srf(path, strict=True)

    def test_val_srf_for_obs(self):
        srf_file = files("glodformat.tests").joinpath(
            "data/W_XX-EUMETSAT-Darmstadt_VIS+IR+SRF_MSG3+SEVIRI_C_EUMG.nc"
        )
        obs_file = files("glodformat.tests").joinpath(
            "data/W_XX-EUMETSAT-Darmstadt,VISNIR+SUBSET+MOON,MSG3+SEVIRI_C_EUMG_20140318140112_01.nc"
        )
        with as_file(srf_file) as srf_path, as_file(obs_file) as obs_path:
            validate_srf_for_obs(srf_path, obs_path, strict=True)


if __name__ == "__main__":
    unittest.main()
