import requests
import os

class DataFetcher:
    def __init__(self, save_directory):
        self.save_directory = save_directory
    
    def fetch_data(self, data_source_url):
        """
        Fetch data from the specified URL and save it to the save_directory.

        Args:
            data_source_url (str): The URL from which to fetch the data.

        Returns:
            str or None: The filepath where the data is saved, or None if the operation fails.

        """
        try:
            os.makedirs(self.save_directory, exist_ok=True)
            
            response = requests.get(data_source_url)
            if response.status_code == 200:
                filename = 'raw_data.json'
                filepath = os.path.join(self.save_directory, filename)
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f"Data downloaded successfully and saved at: {filepath}")
                return filepath
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching data: {str(e)}")
            return None
