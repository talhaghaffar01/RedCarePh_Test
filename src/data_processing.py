from src.schema import ProcessedData, Product
from typing import List, Dict, Any
import json
import os

class DataProcessor:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory

    def process_data(self, filename):
        try:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            output_filename = "processed_raw_data.json"
            output_filepath = os.path.join(self.output_directory, output_filename)
            input_filepath = os.path.join(self.input_directory, filename)

            with open(input_filepath, 'r') as file:
                raw_data = json.load(file)

            processed_data = self._process_json_data(raw_data)

            with open(output_filepath, 'w') as file:
                json.dump(processed_data, file, indent=4)

            print(f"Data processed successfully and saved at: {output_filepath}")
            return output_filepath
        except Exception as e:
            print(f"An error occurred during data processing: {str(e)}")
            return None

    def _process_json_data(self, raw_data: Dict[str, Any]) -> List[ProcessedData]:
        processed_data = []
        for result in raw_data.get('results', []):
            processed_result = ProcessedData(
                application_number=result.get('application_number', ''),
                sponsor_name=result.get('sponsor_name', ''),
                products=[Product(**product) for product in result.get('products', [])]
            )
            processed_data.append(processed_result.dict())  # Convert to dict before appending
        return processed_data
