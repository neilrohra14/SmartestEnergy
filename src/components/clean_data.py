# Data for performing cleaning extracting and validation checks
import pandas as pd
from decimal import Decimal
from src.utils.config import config
from src.exception import CustomException
from src.logger import logging
import sys

class CleanData:
    def __init__(self):
        self.columns_to_extract = config['api']['columns']
        self.expected_data_types = config['api']['data_types']

    def clean(self, json_data):
        
        try:
            if not json_data or "data" not in json_data:
                logging.info("No data available.")
                print("No data available.")
                return None

            # logging.info(json_data)
            cleaned_data = []
            for entry in json_data['data']:
                cleaned_entry = {}
                for column in self.columns_to_extract:
                    if column in entry:
                        value = entry[column]
                        
                        # Blank check
                        if value is None or (isinstance(value, str) and value.strip() == ""):
                            raise CustomException(f"Column '{column}' contains null or blank values.", sys)
                        # logging.info("Blank check complete")

                        # Data type
                        expected_type = self.expected_data_types[column]
                        if not self.validate_data_type(value, expected_type):
                            raise CustomException(f"Column '{column}' has invalid data type. Expected {expected_type}.", sys)
                        # logging.info("Data type validation complete")

                        if expected_type == "decimal":
                            cleaned_entry[column] = Decimal(value)
                        else:
                            cleaned_entry[column] = value

                cleaned_data.append(cleaned_entry)
            logging.info(cleaned_data)
            df = pd.DataFrame(cleaned_data)

            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime'].str.replace('Z', ''))
            logging.info("Cleaning data completed")

            return df
        except KeyError as e:
            raise CustomException(f"Missing expected key: {str(e)}", sys)
        except ValueError as e:
            raise CustomException(f"Value error during data cleaning: {str(e)}", sys)
        except Exception as e:
            raise CustomException(f"An unexpected error occurred during data cleaning: {str(e)}", sys)

    def validate_data_type(self, value, expected_type):
        if expected_type == "str":
            return isinstance(value, str)
        elif expected_type == "decimal":
            try:
                Decimal(value)
                return True
            except:
                return False
        elif expected_type == "int":
            return isinstance(value, int)
        else:
            return False
