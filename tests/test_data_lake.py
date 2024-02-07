import unittest
import os
import json
from unittest.mock import patch, mock_open
from datetime import datetime
from src.data_lake import DataLake
import shutil

class TestDataLake(unittest.TestCase):
    def setUp(self):
        self.base_directory = 'test_data_lake'
        self.processed_directory = os.path.join(self.base_directory, 'processed')
        os.makedirs(self.processed_directory, exist_ok=True)
        self.dlake_directory = os.path.join(self.base_directory, 'dlake')
        os.makedirs(self.dlake_directory, exist_ok=True)
        self.processed_data = [
            {
                'sponsor_name': 'Test Sponsor',
                'products': [
                    {
                        'brand_name': 'Test Brand',
                        'dosage_form': 'Tablet',
                        'marketing_status': 'Approved'
                    }
                ]
            }
        ]
        processed_data_file = os.path.join(self.processed_directory, 'processed_raw_data.json')
        with open(processed_data_file, 'w') as f:
            json.dump(self.processed_data, f)

    @patch('src.data_lake.datetime')
    def test_check_and_update_dlake_json(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        data_lake = DataLake(self.base_directory)
        data_lake.check_and_update_dlake_json()
        dlake_json_file = os.path.join(self.dlake_directory, 'dlake.json')
        self.assertTrue(os.path.exists(dlake_json_file))
        with open(dlake_json_file, 'r') as f:
            updated_data = json.load(f)
        expected_data = [
            {
                'sponsor_name': 'Test Sponsor',
                'brand_name': 'Test Brand',
                'dosage_form': 'Tablet',
                'marketing_status': 'Approved',
                'created_at': '2023-01-01 00:00:00'
            }
        ]
        self.assertEqual(updated_data, expected_data)

    def tearDown(self):
        shutil.rmtree(self.base_directory)

if __name__ == '__main__':
    unittest.main()
