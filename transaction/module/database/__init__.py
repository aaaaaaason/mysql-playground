import os
import pymysql

database = 'playground'

def get_connection(database: str = database, autocommit: bool =True):
    conf = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'cursorclass': pymysql.cursors.DictCursor,
        'connect_timeout': 5,
        'autocommit': autocommit
    }
    if database:
        conf['database'] = database
    return pymysql.connect(**conf)

def init_database(database: str = database):
    with get_connection(database=None) as conn:
        _create_database(conn)

def drop_table(conn, table: str, database: str = database):
    with conn.cursor() as cursor:
        cursor.execute('DROP TABLE %s', (table,))

def _create_database(conn, database: str = database):
    with conn.cursor() as cursor:
        #cursor.execute('CREATE DATABASE IF NOT EXISTS %s', (database,))
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database}', tuple())
        conn.commit()
    