import time
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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function on failure with a specified number of retries and delay.
    
    Args:
        retries: Number of times to retry the function (default: 3).
        delay: Seconds to wait between retries (default: 2).
    
    Returns:
        decorator: The decorator function that wraps the target function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    last_exception = e
                    if attempt < retries:
                        time.sleep(delay)
                        print(f"Retrying ({attempt + 1}/{retries}) after error: {e}")
                    continue
                except Exception as e:
                    raise  
            raise last_exception 
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches all users from the database with retry logic.
    
    Args:
        conn: SQLite database connection.
    
    Returns:
        List of rows from the query result.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"Failed to fetch users: {e}")