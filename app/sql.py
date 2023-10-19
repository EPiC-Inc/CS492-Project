from os import environ

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.sql import text

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

database_url = URL.create(
    f"{dialect}+{framework}",
    username = username,
    password = password,
    host = server,
    port = port,
    database = database,
    query = {
        "driver": driver
    } if driver else {}
)

db = create_engine(database_url)

# with db.begin() as cursor:
#     result = cursor.execute(text("getLogin :email"), {"email": "admin@sms.com"})
#     for row in result:
#         print("a:", row)

# with db.connect() as cursor:
#     result = cursor.execute(text("getLogin :email"), {"email": "admin@sms.com"})
#     for row in result:
#         print("a:", row)

# db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

def query_db(command: str, **kwargs) -> list:
    ''' <command> is entered as storedProcedure :argument1, :argument2 '''
    result = []
    with db.connect() as cursor:
        response = cursor.execute(text(command), kwargs)
        for row in response:
            result.append(row)
    return result

def execute_db(command: str, **kwargs) -> list:
    ''' <command> is entered as storedProcedure :argument1, :argument2 '''
    result = []
    with db.begin() as cursor:
        response = cursor.execute(text(command), kwargs)
        for row in response:
            result.append(row)
    return result
