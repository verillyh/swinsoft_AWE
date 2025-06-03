import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, db_name: str, user: str, password: str, host="feenix-mariadb.swin.edu.au"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.conn = None
        self.cursor = None
        self.state = False

    # + connect(db_name: String): Boolean
    def connect(self, db_name: str) -> bool:
        if self.state:
            print("⚠️ Already connected.")
            return False
        if db_name != self.db_name:
            print("❌ Database name mismatch.")
            return False

        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            self.cursor = self.conn.cursor()
            self.state = True
            print(f"✅ Connected to database: {self.db_name}")
            return True
        except Error as e:
            print(f"❌ Connection failed: {e}")
            return False

    # + disconnect(db_name: String): Boolean
    def disconnect(self, db_name: str) -> bool:
        if self.state and db_name == self.db_name:
            try:
                self.cursor.close()
                self.conn.close()
                self.state = False
                print(f"🔌 Disconnected from database: {db_name}")
                return True
            except Error as e:
                print(f"❌ Disconnection failed: {e}")
        else:
            print("⚠️ Disconnection failed or already disconnected.")
        return False

    # + query(query: String): List[tuple] or List[str]
    def query(self, query: str, params=None):
        if not self.state:
            print("❌ Error: Not connected.")
            return []

        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return ["✅ Query executed successfully."]
        except Error as e:
            print(f"❌ Query failed: {e}")
            return []

