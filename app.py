from flask import Flask, jsonify, request, abort
from src.data_fetch import DataFetcher
from src.data_processing import DataProcessor
from src.data_lake import DataLake
import os
import json
from functools import wraps


app = Flask(__name__)

# Initialize your fetcher, processor, and data lake objects
fetcher = DataFetcher('data/raw')
processor = DataProcessor('data/raw', 'data/processed')
data_lake = DataLake('data')

# Define your secret token (you can retrieve this from environment variables in production)
# SECRET_TOKEN = "your_secret_token" (for local testing)
SECRET_TOKEN = os.getenv('SECRET_TOKEN')

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') != SECRET_TOKEN:
            return jsonify({'message': 'Authentication failed'}), 401
        return f(*args, **kwargs)
    return decorated_function


# Route to check the status of the application
@app.route('/', methods=['GET'])
def check_status():
    """
    Check if the application is up.
    """
    return jsonify({'message': 'Application is up!'}), 200

# Route to fetch data
@app.route('/fetch-data', methods=['POST'])
@authenticate
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

# Route to process data
@app.route('/process-data', methods=['POST'])
@authenticate
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

# Route to store data
@app.route('/store-data', methods=['POST'])
@authenticate
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

# Route to get dlake.json data
@app.route('/dlake-json', methods=['GET'])
@authenticate
def get_dlake_json():
    """
    Returns the JSON data present in data/dlake/dlake.json.

    Returns:
        JSON response containing the data from dlake.json or an error message if the file is not found.
    """
    dlake_json_file = os.path.join('data', 'dlake', 'dlake.json')
    if os.path.exists(dlake_json_file):
        with open(dlake_json_file, 'r') as f:
            dlake_data = json.load(f)
        return jsonify(dlake_data), 200
    else:
        return jsonify({'message': 'No result found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
