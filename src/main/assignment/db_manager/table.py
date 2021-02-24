import datetime
import pandas as pd


class Table:
    """A Postgres table.
    """

    def __init__(self, name, db):
        """
        Args:
            name (string): name of the table
            db (DataBase): parent database
        Attrs:
            name (string): name of the table
            db (DataBase): parent database
            server (Server): parent server
        """
        self.name = name
        self.db = db
        self.server = db.server
        self.structure = [
            x
            for x in self.get_structure()["column_name"].tolist()
        ]

    def download(self, condition=None):
        """
        Action:
            Downloads the table
        Return:
            pandas dataframe
        """
        if condition is None:
            statement = """
                SELECT *
                FROM {}.{}
                """.format(
                self.db.name, self.name
            )
        else:
            statement = """
                SELECT *
                FROM {}.{}
                WHERE {}
                """.format(
                self.db.name, self.name, condition
            )
        return self.server._execute_extract(statement)

    def append_dataframe(self, df):
        if not set(list(df)) - set(self.structure):
            self.db.start_engine()
            try:
                df.to_sql(
                    self.name,
                    self.db.engine,
                    schema=self.db.name,
                    if_exists="append",
                    index=False,
                    method="multi",
                )
            except Exception as e:
                print(e.args[0])
                raise ValueError("I have raised an Exception")
                return 0
            self.db.stop_engine()
            return 1
        else:
            print("you dataframe has different columns than the sql table")
            print("Extra columns of your df:", set(list(df)) - set(self.structure))
            return 0

    def get_structure(self):
        statement = """
        select column_name from information_schema.columns where table_schema = \'{}\' and table_name = \'{}\';
        """.format(
            self.db.name, self.name
        )

        return self.server._execute_extract(statement)

