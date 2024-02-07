import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    @patch('src.data_fetch.DataFetcher.fetch_data')
    def test_fetch_data_success(self, mock_fetch_data):
        # Test fetching data successfully
        mock_fetch_data.return_value = 'data/raw/test_data.json'

        tester = app.test_client(self)
        response = tester.post('/fetch-data', json={'data_source_url': 'mocked_url'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data fetched successfully', response.data)

    @patch('src.data_processing.DataProcessor.process_data')
    def test_process_data_success(self, mock_process_data):
        # Test processing data successfully
        mock_process_data.return_value = 'data/processed/processed_test_data.json'

        tester = app.test_client(self)
        response = tester.post('/process-data', json={'input_filename': 'test_data.json'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data processed successfully', response.data)

    @patch('src.data_lake.DataLake.check_and_update_dlake_json')
    def test_store_data_success(self, mock_check_and_update):
        # Test storing data successfully
        mock_check_and_update.return_value = None

        tester = app.test_client(self)
        response = tester.post('/store-data')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data stored successfully', response.data)

if __name__ == '__main__':
    unittest.main()
