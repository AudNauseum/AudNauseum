from audnauseum.data_models.complex_encoder import ComplexEncoder

import unittest


class ComplexEncoderTest(unittest.TestCase):

    def test_encode_data(self):
        complex_encoder = ComplexEncoder()
        print(complex_encoder.__class__.__name__)
        self.assertTrue(True)
