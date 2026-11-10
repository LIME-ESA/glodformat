import unittest
from importlib.resources import files, as_file

from glodformat.srf import validate_srf


class TestSRF(unittest.TestCase):
    def test_val_srf(self):
        data_file = files("glodformat.tests").joinpath("data/W_XX-EUMETSAT-Darmstadt_VIS+IR+SRF_MSG3+SEVIRI_C_EUMG.nc")   
        with as_file(data_file) as path:
            validate_srf(path, strict=True)

if __name__ == "__main__":
    unittest.main()
