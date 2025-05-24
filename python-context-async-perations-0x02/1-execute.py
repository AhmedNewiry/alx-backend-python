import sqlite3

class ExecuteQuery:
    """
    A class-based context manager for executing a specific SQL query with parameters.
    """
    def __init__(self, db_name, query, params=()):
        """
        Initialize the context manager with database name, query, and parameters.
        
        Args:
            db_name (str): The name of the SQLite database file.
            query (str): The SQL query to execute.
            params (tuple): Parameters for the query (default: empty tuple).
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Open the database connection, execute the query, and return the results.
        
        Returns:
            list: The results of the query.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection and commit or rollback based on exceptions.
        
        Args:
            exc_type: The type of the exception that occurred, if any.
            exc_value: The instance of the exception that occurred, if any.
            traceback: The traceback of the exception that occurred, if any.
        """
        try:
            if exc_type is not None:
                self.conn.rollback()
                print(f"Exception occurred: {exc_type.__name__}: {exc_value}")
            else:
                self.conn.commit()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

if __name__ == "__main__":
    try:
        with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
            print("Users older than 25:", results)
    except Exception as e:
        print(f"Failed to execute query: {e}")