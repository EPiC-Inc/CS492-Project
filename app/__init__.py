from configparser import ConfigParser
from os import environ
from types import SimpleNamespace

from flask import Flask

app = Flask(__name__)

# Read in the configuration file
config_parser = ConfigParser()
config_parser.read("app/configuration.ini")
config = SimpleNamespace(**config_parser.defaults())

app.secret_key = environ['MGMT_SECRET_KEY']

@app.context_processor
def allow_access_to_global_variables_in_templates() -> dict:
    return {
        "school_name": config.school_name
    }

from . import routes
