from flask import Flask
from os import environ

app = Flask(__name__)
app.secret_key = environ.get("MGMT_SECRET_KEY", AssertionError("Please make sure a secret key is configured with the environment variable MGMT_SECRET_KEY"))

from . import routes