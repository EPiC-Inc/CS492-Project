from flask import Flask
from configparser import ConfigParser
from types import SimpleNamespace
from os import environ

app = Flask(__name__)

# Read in the configuration file
config_parser = ConfigParser()
config_parser.read("app/configuration.ini")
config = SimpleNamespace(**config_parser.defaults())

app.secret_key = environ['MGMT_SECRET_KEY']

@app.context_processor
def allow_access_in_templates():
    return {
        "school_name": config.school_name
    }

from . import routes