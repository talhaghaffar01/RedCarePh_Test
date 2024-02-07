import unittest
import os
import tempfile
from unittest.mock import patch, mock_open
from src.data_fetch import DataFetcher
from requests import Session
from requests_cache import CachedSession
import requests

class TestDataFetcher(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_directory = self.temp_dir.name
        self.fetcher = DataFetcher(self.save_directory)

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('src.data_fetch.CachedSession.get')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    def test_fetch_data_success(self, mock_open, mock_requests_get):
        # Test fetching data successfully
        mock_requests_get.return_value.status_code = 200
        data_source_url = 'https://example.com/data.json'
        filepath = self.fetcher.fetch_data(data_source_url)
        mock_requests_get.assert_called_once_with(data_source_url)
        self.assertIsNotNone(filepath)
        self.assertTrue(filepath.startswith(self.save_directory))
        mock_open.assert_called_once_with(filepath, 'wb')

    @patch('src.data_fetch.CachedSession.get')
    def test_fetch_data_failure(self, mock_requests_get):
        # Test fetching data failure
        mock_requests_get.return_value.status_code = 404
        data_source_url = 'https://example.com/nonexistent.json'
        filepath = self.fetcher.fetch_data(data_source_url)
        mock_requests_get.assert_called_once_with(data_source_url)
        self.assertIsNone(filepath)

    @patch('src.data_fetch.CachedSession.get', side_effect=requests.exceptions.RequestException)
    def test_fetch_data_exception(self, mock_requests_get):
        # Test fetching data exception
        data_source_url = 'https://example.com/exception.json'
        filepath = self.fetcher.fetch_data(data_source_url)
        mock_requests_get.assert_called_once_with(data_source_url)
        self.assertIsNone(filepath)

if __name__ == '__main__':
    unittest.main()
