from sqlalchemy import create_engine
from .table import Table


class DataBase:
    """A Postgres database.
    """

    def __init__(self, name, server):
        """
        Args:
            name (string): name of the database
            server (Server): parent server
        Attrs:
            name (string)
            server(Server)
            tb (dict): dict of the tables on the database {name (str) : table (Table)}
        """
        self.name = name
        self.server = server
        self.tb = {x: Table(x, self) for x in self._get_tables()["tablename"]}

    def _get_tables(self):
        return self.server._execute_extract(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = '{}'".format(
                self.name
            )
        )

    def show_tables(self):
        return list(self.tb.keys())

    def start_engine(self):
        cmd = f"postgres+psycopg2://{self.server.user}:{self.server.passwd}@{self.server.ip}:5432/{self.server.database}"
        self.engine = create_engine(cmd)
        self.engine_state = "started"

    def stop_engine(self):
        self.engine.dispose()
        self.engine_state = "stopped"
