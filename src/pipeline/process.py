import sys
import threading
from datetime import datetime, timedelta
from src.components.external import External
from src.components.clean_data import CleanData
from src.logger import logging
from src.exception import CustomException

def process_data(target_date=None):
    try:
        if target_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime('%Y-%m-%d')  # Format date as 'yyyy-mm-dd'

        def background_task():
            external = External()
            response_df = external.fetch_data(target_date)

            cleaner = CleanData()
            try:
                cleaned_df = cleaner.clean(response_df)
                if cleaned_df is not None:
                    logging.info(f"Cleaned data for {target_date}: {cleaned_df.head()}")
                else:
                    logging.info(f"No data available for {target_date}")
            except CustomException as e:
                logging.error(f"Data cleaning failed: {str(e)}")

        thread = threading.Thread(target=background_task)
        thread.start()
        return f"Processing for {target_date} started, continuing in background"
    except Exception as ex:
        raise CustomException(ex, sys)



if __name__ == "__main__":
    process_data()
