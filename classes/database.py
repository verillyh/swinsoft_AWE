class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.state = False  # False = disconnected, True = connected

    def connect(self, db_name: str) -> bool:
        if db_name == self.db_name:
            self.state = True
            print(f"Connected to database: {db_name}")
            return True
        print(f"Failed to connect to database: {db_name}")
        return False

    def disconnect(self, db_name: str) -> bool:
        if self.state and db_name == self.db_name:
            self.state = False
            print(f"Disconnected from database: {db_name}")
            return True
        print(f"Failed to disconnect from database: {db_name}")
        return False

    def query(self, query: str) -> str:
        if not self.state:
            return "Error: Not connected to any database."
        # Simulate returning query results
        return f"Result of query '{query}' on database '{self.db_name}'"
