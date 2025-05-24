import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for handling SQLite database connections.
    """
    def __init__(self, db_name):
        """
        Initialize the context manager with the database name.
        
        Args:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Open the database connection and create a cursor.
        
        Returns:
            cursor: The SQLite cursor object for executing queries.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

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
        with DatabaseConnection('users.db') as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print("Users:", results)
    except Exception as e:
        print(f"Failed to fetch users: {e}")