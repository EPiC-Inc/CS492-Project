from os import environ

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.sql import text
from sqlalchemy.exc import ResourceClosedError

from . import config

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

def query_db(command: str, **kwargs) -> list:
    ''' <command> is entered as storedProcedure :argument1, :argument2 \n
     <kwargs> will fill in the arguments i.e. argument1='blah' '''
    result = []
    with db.connect() as cursor:
        response = cursor.execute(text(command), kwargs)
        for row in response:
            result.append(row)
    return result

def execute_db(command: str, **kwargs) -> list:
    ''' <command> is entered as storedProcedure :argument1, :argument2 \n
     <kwargs> will fill in the arguments i.e. argument1='blah' '''
    result = []
    with db.begin() as cursor:
        response = cursor.execute(text(command), kwargs)
        try:
            for row in response:
                result.append(row)
        except ResourceClosedError:
            pass
    return result
