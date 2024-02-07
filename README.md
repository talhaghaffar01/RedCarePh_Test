# Redcare Pharmaceutical Data Processing Application

## Overview
This is a Flask-based application for fetching, processing, and storing pharmaceutical data. The application utilizes Docker for easy deployment and management.

## Application Flow

- **Data Fetching**:
  - The application fetches raw data from a specified URL, typically containing pharmaceutical information.

- **Data Processing**:
  - The fetched data undergoes processing to normalize it into a structured format.
  - Relevant information such as application numbers, sponsor names, and product details are extracted and organized.

- **Data Storage**:
  - Processed data is stored in a data lake, which serves as a centralized repository.
  - Only essential details needed for analysis are stored, optimizing storage resources.

- **Handling New Data Fetches**:
  - When new data is fetched, the application appends it to existing data in the data lake, avoiding duplicates.

- **Viewing Data**:
  - Users can access a GET endpoint to view the current contents of the data lake.
  - This allows for easy review and analysis of stored pharmaceutical data.

## Getting Started
To run the application locally, follow these steps:

1. Clone this repository:
    ```
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```
    cd <project_directory>
    ```

3. Build the Docker image:
    ```
    docker build --tag redcare .
    ```

4. Run the Docker container:
    ```
    docker run -d -p 5000:5000 redcare
    ```

## Sample Requests

### Fetch Data
```python
import requests

url = 'http://localhost:5000/fetch-data'
headers = {
    'Authorization': 'token_here',  # Replace token_here with the token from the Dockerfile
    'Content-Type': 'application/json' 
}
payload = {
    'data_source_url': 'https://api.fda.gov/drug/drugsfda.json?search=products.dosage_form:"LOTION"&limit=1'
}
response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
```

### Process Data
```python
import requests

base_url = 'http://localhost:5000'
secret_token = 'token_here'  # Replace token_here with the token from the Dockerfile

process_data_payload = {
    'input_filename': 'raw_data.json'  
}

headers = {
    'Authorization': secret_token,
    'Content-Type': 'application/json'
}

process_data_response = requests.post(f'{base_url}/process-data', json=process_data_payload, headers=headers)
print(process_data_response.status_code)
print(process_data_response.json())
```

### Store Data to DataLake
```python
import requests
url = 'http://localhost:5000/store-data'
headers = {
    'Authorization': 'abc123', # Replace token_here with the token from the Dockerfile
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers)
print('Response status code:', response.status_code)
print('Response content:', response.json())
```

### View Data in Datalake
```python
import requests

url = 'http://localhost:5000/dlake-json'
headers = {
    'Authorization': 'token'  # Replace token_here with the token from the Dockerfile
}
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())
```

