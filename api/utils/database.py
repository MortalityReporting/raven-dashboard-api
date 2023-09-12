from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection
from sqlalchemy.exc import OperationalError, IntegrityError, ProgrammingError
from os import getenv

def create_connection(return_engine: bool = False) -> Engine | Connection | str:
    '''Create a connection and return either the connection or the engine'''
    db_conn_string = getenv("DB_CONN_STRING")
    print(db_conn_string)
    engine: Engine = create_engine(db_conn_string, echo=True)
    try:
        connection: Connection = engine.connect()
        if return_engine:
            return engine
        else:
            print(connection)
            return connection
    except OperationalError as e:
        return str(e)