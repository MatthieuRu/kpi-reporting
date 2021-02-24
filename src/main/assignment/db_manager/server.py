import pandas as pd
import sqlalchemy
from .database import DataBase
from sqlalchemy.sql import text


class Server:
    def __init__(self, ip, user, passwd, database):
        self.ip = ip
        self.database = database
        self.user = user
        self.passwd = passwd
        self.connection = self._get_connection()
        self.db = self._get_databases()

    def _get_databases(self):
        return {
            x: DataBase(x, self)
            for x in self._show_databases()["schema_name"]
            if x
            not in ["information_schema", "pg_catalog", "pg_toast", "piblic"]
        }

    def _execute_action(self, action):
        self.connection.execute(action)
        return 1

    def _get_connection(self):
        conn_str = f"postgres+psycopg2://{self.user}:{self.passwd}@{self.ip}:5432/{self.database}"
        engine = sqlalchemy.create_engine(conn_str)
        return engine.connect()

    def _execute_extract(self, action):
        return pd.read_sql(action, self.connection)

    def _show_databases(self):
        return self._execute_extract(
            "select schema_name from information_schema.schemata;"
        )

    def _create_schema_abc(self, filename):
        file = open(filename)
        query = text(file.read())
        self._execute_action(query)
        self.db = self._get_databases()
        return 1

    def _delete_schema_abc(self):
        query = """drop schema abc cascade;"""
        self._execute_action(query)
        self.db = self._get_databases()
        return 1
