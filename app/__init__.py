from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from types import SimpleNamespace
from os import environ

app = Flask(__name__)

# Read in the configuration file
config_parser = ConfigParser()
config_parser.read("app/configuration.ini")
config = SimpleNamespace(**config_parser.defaults())

app.secret_key = environ.get("MGMT_SECRET_KEY", AssertionError("Please make sure a secret key is configured with the environment variable MGMT_SECRET_KEY"))

# Set up the database connection
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = f"{config.sqlalchemy_driver}://{config.database_user}:{environ.get('SCHOOL_MANAGEMENT_DB_PASS', AssertionError('''Please make sure a databse password is configured with the environment variable SCHOOL_MANAGEMENT_DB_PASS'''))}@{config.database_url}/{config.database_name}"
db.init_app(app) #FIXME

@app.context_processor
def allow_access_in_templates():
    return {
        "school_name": config.school_name
    }

from . import routes