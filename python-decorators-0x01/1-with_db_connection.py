import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that handles opening and closing a SQLite database connection.
    
    Args:
        func: The function to be decorated, which uses a database connection.
    
    Returns:
        wrapper: The wrapped function that passes a connection object to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit any changes
            return result
        except Exception as e:
            if conn:
                conn.rollback()  # Rollback on error
            raise
        finally:
            if conn:
                conn.close()  # Always close the connection
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user by ID from the database.
    
    Args:
        conn: SQLite database connection.
        user_id: The ID of the user to fetch.
    
    Returns:
        Tuple containing the user data or None if not found.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    try:
        user = get_user_by_id(user_id=1)
        print(user)
    except Exception as e:
        print(f"Failed to fetch user: {e}")