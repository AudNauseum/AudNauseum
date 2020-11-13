from audnauseum.data_models.complex_decoder import ComplexDecoder

import unittest


class ComplexDecoderTest(unittest.TestCase):

    def test_encode_data(self):
        complex_decoder = ComplexDecoder()
        print(complex_decoder.__class__.__name__)
        self.assertTrue(True)
