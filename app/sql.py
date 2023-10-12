import pyodbc
from . import app, config
from os import environ

# Set up the database connection
server = config.database_url
database = config.database_name
username = config.database_user
password = environ['SCHOOL_MANAGEMENT_DB_PASS']
driver = config.database_driver

db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
