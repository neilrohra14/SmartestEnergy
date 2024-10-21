import sys
import threading
from datetime import datetime, timedelta
from src.components.external import External
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

        thread = threading.Thread(target=background_task)
        thread.start()
        return f"Processing for {target_date} started, continuing in background"
    except Exception as ex:
        raise CustomException(ex, sys)


if __name__ == "__main__":
    process_data()
