import sys
import threading
from src.components.external import External
from src.logger import logging
from src.exception import CustomException

def process_data():
    try:
        def background_task():
            external = External()
            target_date = "2024-02-01"
            response_df = external.fetch_data(target_date)
        
        thread = threading.Thread(target= background_task)

        thread.start()
        return "Processing started, continuing in background"
    except Exception as ex:
        raise CustomException(ex, sys)




if __name__ == "__main__":
    process_data()
    # print(response_df)


    # obj=DataInjection()
    # raw, df = obj.initiate_data_injection('notebook/data/Data Engineer Task.xlsx')

    # transformation = DataTransformation()
    # h, m, c, s = transformation.initiate_data_transformation(df)

    # load = DataLoad()
    # file_path = load.initiate_data_load(h, m, c, s)
    