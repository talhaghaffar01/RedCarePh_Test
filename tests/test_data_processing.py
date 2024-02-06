import unittest
import os
import tempfile
import json
from src.data_processing import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        # Set up temporary directories and example JSON data for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_directory = os.path.join(self.temp_dir.name, 'input')
        self.output_directory = os.path.join(self.temp_dir.name, 'output')
        os.makedirs(self.input_directory, exist_ok=True)
        os.makedirs(self.output_directory, exist_ok=True)
        self.raw_data = {"meta": {"disclaimer": "Do not rely on openFDA to make decisions regarding medical care..."},
                         "results": [{"application_number": "NDA009895", "sponsor_name": "BAYER PHARMS", "products": []},
                                     {"application_number": "ANDA087644", "sponsor_name": "DOW PHARM", "products": []}]}
        with open(os.path.join(self.input_directory, 'test_data.json'), 'w') as f:
            json.dump(self.raw_data, f)

    def test_data_processing(self):
        # Test the data processing functionality
        processor = DataProcessor(self.input_directory, self.output_directory)
        input_filename = 'test_data.json'
        output_filepath = processor.process_data(input_filename)
        self.assertTrue(os.path.exists(output_filepath))

    def tearDown(self):
        # Clean up temporary directory after testing
        self.temp_dir.cleanup()

if __name__ == '__main__':
    unittest.main()
