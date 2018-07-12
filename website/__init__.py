import os
from flask import Flask

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('config.py')

from website import views