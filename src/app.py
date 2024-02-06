from flask import Flask, jsonify, request
from src.data_fetch import DataFetcher
from src.data_processing import DataProcessor
from src.data_lake import DataLake
import os

app = Flask(__name__)


fetcher = DataFetcher('data/raw')
processor = DataProcessor('data/raw', 'data/processed')
data_lake = DataLake('data')

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    """
    Fetches data from a specified data source URL.

    Returns:
        JSON response indicating success or failure of data fetching.
    """
    try:
        data = request.json
        data_source_url = data.get('data_source_url')
        if data_source_url:
            filepath = fetcher.fetch_data(data_source_url)
            if filepath:
                return jsonify({'message': 'Data fetched successfully', 'filepath': filepath}), 200
            else:
                return jsonify({'message': 'Failed to fetch data'}), 400
        else:
            return jsonify({'message': 'Data source URL not provided'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/process-data', methods=['POST'])
def process_data():
    """
    Processes the fetched data.

    Returns:
        JSON response indicating success or failure of data processing.
    """
    try:
        data = request.json
        input_filename = data.get('input_filename')
        if input_filename:
            output_filepath = processor.process_data(input_filename)
            if output_filepath:
                return jsonify({'message': 'Data processed successfully', 'output_filepath': output_filepath}), 200
            else:
                return jsonify({'message': 'Failed to process data'}), 400
        else:
            return jsonify({'message': 'Input filename not provided'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/store-data', methods=['POST'])
def store_data():
    """
    Stores the processed data.

    Returns:
        JSON response indicating success or failure of data storage.
    """
    try:
        processed_data_path = os.path.join('data', 'processed', 'processed_raw_data.json')
        data_lake.check_and_update_dlake_json()

        return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
