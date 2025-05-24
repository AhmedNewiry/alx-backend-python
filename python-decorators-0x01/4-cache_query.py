import time
import sqlite3
import functools

query_cache = {}

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

def cache_query(func):
    """
    Decorator that caches database query results based on the SQL query string.
    
    Args:
        func: The function to be decorated, which executes a database query.
    
    Returns:
        wrapper: The wrapped function that checks the cache before executing the query.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = None
        if args and len(args) > 1 and isinstance(args[1], str):
            query = args[1]
        elif 'query' in kwargs and isinstance(kwargs['query'], str):
            query = kwargs['query']
        
        if not query:
            raise ValueError("No query found in function arguments")
        
        if query in query_cache:
            print(f"Returning cached result for query: {query}")
            return query_cache[query]
        
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database with caching based on the query string.
    
    Args:
        conn: SQLite database connection.
        query: The SQL query to execute.
    
    Returns:
        List of rows from the query result.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    try:
        users = fetch_users_with_cache(query="SELECT * FROM users")
        print("First call:", users)

        users_again = fetch_users_with_cache(query="SELECT * FROM users")
        print("Second call:", users_again)
    except Exception as e:
        print(f"Failed to fetch users: {e}")