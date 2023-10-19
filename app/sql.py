from os import environ
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.sql import text
from unittest import result

import pyodbc

from . import app, config

# Set up the database connection
dialect = config.database_dialect
framework = config.database_framework
username = config.database_user
password = environ['SCHOOL_MANAGEMENT_DB_PASS']
server = config.database_url
port = config.database_port
database = config.database_name
driver = config.database_driver

# database_url = URL.create(
#     f"{dialect}+{framework}",
#     username = username,
#     password = password,
#     host = server,
#     port = port,
#     database = database,
#     query = {
#         "driver": driver
#     } if driver else {}
# )

# engine = create_engine(database_url)
# with engine.begin() as cursor:
#     result = cursor.execute(text("getLogin"), [("?", "admin@sms.com")])
#     for row in result:
#         print("a:", row.username)

# with engine.connect() as cursor:
#     result = cursor.execute(text("getLogin"), ('admin@sms.com'))
#     for row in result:
#         print("username:", row.username)
 

# exit()


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
