import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from flask import Flask, request, render_template
from src.routes.daily_report import daily_report

# Create the Flask application
app = Flask(__name__)


app.register_blueprint(daily_report, url_prefix='/api')


# Default route url is http://127.0.0.1:5000
@app.route('/')
def index():
    return "Welcome to the Daily Report API!"

if __name__ == '__main__':
    app.run(debug=True)
