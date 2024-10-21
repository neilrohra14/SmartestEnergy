import sys
from flask import Blueprint, jsonify, request
from src.logger import logging
from src.exception import CustomException
from src.pipeline.process import process_data


daily_report = Blueprint('daily_report', __name__)

@daily_report.route('/daily-report', methods=['GET'])
def get_daily_report():
    try:

        target_date = request.args.get('date', "2024-02-01")  # Default date if not provided

        # Call the process_data function and pass the target date
        result_message = process_data(target_date)
        return jsonify({"message": result_message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    except Exception as ex:
        raise CustomException(ex, sys)
