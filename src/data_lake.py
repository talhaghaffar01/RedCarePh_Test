import os
import shutil
import json

from datetime import datetime

class DataLake:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.dlake_directory = os.path.join(self.base_directory, 'dlake')

    def create_dlake_directory(self):
        os.makedirs(self.dlake_directory, exist_ok=True)

    def check_and_update_dlake_json(self):
        try:
            dlake_json_file = os.path.join(self.dlake_directory, 'dlake.json')
            processed_data_file = os.path.join(self.base_directory, 'processed', 'processed_raw_data.json')

            # Check if dlake directory exists, create if not
            if not os.path.exists(self.dlake_directory):
                self.create_dlake_directory()

            # Load existing data from dlake.json if it exists
            if os.path.exists(dlake_json_file):
                with open(dlake_json_file, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            # Load data from processed data file
            with open(processed_data_file, 'r') as f:
                processed_data = json.load(f)

            # Append new entries from processed data to existing_data if they are not already present
            for entry in processed_data:
                sponsor_name = entry['sponsor_name']
                products = entry['products']
                for product in products:
                    product_info = {
                        'sponsor_name': sponsor_name,
                        'brand_name': product['brand_name'],
                        'dosage_form': product['dosage_form'],
                        'marketing_status': product['marketing_status'],
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    # Check if an entry with the same relevant fields already exists in existing_data
                    if not any(
                        d['sponsor_name'] == product_info['sponsor_name'] and
                        d['brand_name'] == product_info['brand_name'] and
                        d['dosage_form'] == product_info['dosage_form'] and
                        d['marketing_status'] == product_info['marketing_status']
                        for d in existing_data
                    ):
                        existing_data.append(product_info)

            # Write the updated data to dlake.json
            with open(dlake_json_file, 'w') as f:
                json.dump(existing_data, f, indent=4)

            print(f"Updated dlake.json with new data from {processed_data_file}")
        except Exception as e:
            print(f"An error occurred while updating dlake.json: {str(e)}")
