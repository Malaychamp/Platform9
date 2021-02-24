import sqlite3


class ConnectDB:

    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        try:
            conn_obj = sqlite3.connect(self.db_name)
        except Exception as e:
            print("Error in connecting to SQLite DB : ", self.db_name)
            print("Error : ", e)
        else:
            return conn_obj
