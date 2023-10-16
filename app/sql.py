from os import environ
from unittest import result

import pyodbc

from . import app, config

# Set up the database connection
server = config.database_url
database = config.database_name
username = config.database_user
password = environ['SCHOOL_MANAGEMENT_DB_PASS']
driver = config.database_driver

db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

def query_db(command) -> list:
    #FIXME: SQLi
    result = []
    cursor = db.cursor()
    response = cursor.execute(command)
    while (row := cursor.fetchone()):
        result.append(row)
    return result

def execute(command) -> None:
    #FIXME: SQLi
    cursor = db.cursor()
    response = cursor.execute(command)
    cursor.commit()
