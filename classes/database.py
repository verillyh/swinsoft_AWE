class Database:
    def __init__(self, db_name: str):
        self._db_name = db_name  # underscore indicates internal use
        self.state = False       # False = disconnected, True = connected

    # + connect(db_name: String): Boolean
    def connect(self, db_name: str) -> bool:
        if db_name == self._db_name and not self.state:
            self.state = True
            print(f"Connected to database: {db_name}")
            return True
        print("Connection failed or already connected.")
        return False

    # + disconnect(db_name: String): Boolean
    def disconnect(self, db_name: str) -> bool:
        if self.state and db_name == self._db_name:
            self.state = False
            print(f"Disconnected from database: {db_name}")
            return True
        print("Disconnection failed or already disconnected.")
        return False

    # + query(query: String): String
    def query(self, query: str) -> str:
        if not self.state:
            return "Error: Not connected to any database."
        # Simulate processing a query
        print(f"Running query: {query}")
        return f"Result of query: '{query}' on '{self._db_name}'"
