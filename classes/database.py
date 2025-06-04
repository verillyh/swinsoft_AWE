import pymysql
from pymysql.err import MySQLError

class Database:
    def __init__(self, db_name: str):
        self._db_name = db_name
        self.state = False
        self.conn = None

    def connect(self, db_name: str):
        if db_name != self._db_name:
            print("Database name mismatch.")
            return False

        try:
            self.conn = pymysql.connect(
                host="localhost",      
                port=3306,               
                user="root",   
                password="root",
                database=db_name,       
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.state = True
            print(f"Connected to MySQL schema: {db_name}")
            return True
        except MySQLError as e:
            print("Connection error:", e)
            return False

    def disconnect(self, db_name: str) -> bool:
        if not self.state or db_name != self._db_name or self.conn is None:
            print("Cannot disconnect (either not connected or wrong name).")
            return False
        self.conn.close()
        self.state = False
        print(f"Disconnected from MySQL schema: {db_name}")
        return True

    def query(self, sql: str, params: tuple = None):
        try:
            with self.conn.cursor() as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                
                if sql.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                else:
                    self.conn.commit()
                    return True
        except Exception as e:
            print("SQL error:", e)
            return False
