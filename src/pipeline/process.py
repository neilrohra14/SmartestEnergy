import sys
import threading
from datetime import datetime, timedelta
from src.components.external import External
from src.components.clean_data import CleanData
from src.components.analysis import AnalyseData
from src.utils.utils import save_cleaned_data_to_excel, open_excel_file
from src.logger import logging
from src.exception import CustomException
import os


def process_data(target_date=None):  # Optional parameter for the date
    try:
        # If no target date is provided, set it to yesterday's date
        if target_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime('%Y-%m-%d')  # Format date as 'yyyy-mm-dd'

        def background_task():
            external = External()
            response_df = external.fetch_data(target_date)

            # Clean the data using CleanData class
            cleaner = CleanData()
            try:
                cleaned_df = cleaner.clean(response_df)
                if cleaned_df is not None:
                    logging.info(f"Cleaned data for {target_date}: {cleaned_df.head()}")
                    
                    # Save the cleaned data to Excel
                    file_path = os.path.join(os.getcwd(), 'artifacts', 'cleaned_data.xlsx')
                    save_cleaned_data_to_excel(cleaned_df, target_date)

                    # Analyse the data and save the chart
                    analyser = AnalyseData(cleaned_df)
                    analyser.save_chart_to_excel(target_date)

                    # Generate and save the imbalance summary
                    analyser.save_summary_to_excel(target_date)
                    
                    # Automatically open the Excel file after processing
                    open_excel_file(file_path)

                else:
                    logging.info(f"No data available for {target_date}")
            except CustomException as e:
                logging.error(f"Data cleaning failed: {str(e)}")
                raise CustomException(f"Error during data processing: {str(e)}")

        thread = threading.Thread(target=background_task)
        thread.start()
        return f"Processing for {target_date} started, continuing in background"
    except Exception as ex:
        raise CustomException(ex, sys)


if __name__ == "__main__":
    process_data()
