# A file for all external APIs/calls
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
import requests
from src.utils.config import config

@dataclass
class ExternalConfig:
    base_url: str = config['api']['base_url']
    api_format: str = config['api']['format']  

class External:
    def __init__(self):
        self.config = ExternalConfig()

    def fetch_data(self, target_date: str):

        # Validate the date format before proceeding
        if not self.is_valid_date(target_date):
            raise ValueError("Date must be in 'yyyy-mm-dd' format.")
        
        url = f"{self.config.base_url}{target_date}?format={self.config.api_format}"
        
        try:
            # headers = {
            #     # 'Authorization': 'Bearer your_api_token_here',
            #     # 'Content-Type': 'application/json',
            # }
            
            response = requests.get(url) 
            response.raise_for_status()
            # logging.info(response.json())
            logging.info(f"Response received successfully for date: {target_date}")

            # response_df = response.json
            # logging.info('Json is')
            # logging.info(response.json())
            return response.json()
        
        except Exception as ex:
            raise CustomException(ex, sys)

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

# if __name__ == "__main__":
#     external = External()
#     target_date = "2024-02-01"
#     response_df = external.fetch_data(target_date)

#     if response_df is not None:
#         print(response_df)  # Print the first few rows of the DataFrame
#     else:
#         print("Failed to fetch data.")
