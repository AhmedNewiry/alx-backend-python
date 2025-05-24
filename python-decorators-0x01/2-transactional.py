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
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that ensures a function runs within a database transaction.
    Commits on success, rolls back on failure.
    
    Args:
        func: The function to be decorated, which performs a database operation.
    
    Returns:
        wrapper: The wrapped function that manages the transaction.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = args[0]  
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.commit()  
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email in the database.
    
    Args:
        conn: SQLite database connection.
        user_id: The ID of the user to update.
        new_email: The new email address.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


if __name__ == "__main__":
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("Email updated successfully")
    except Exception as e:
        print(f"Failed to update email: {e}")