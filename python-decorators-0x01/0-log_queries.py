import sqlite3
import functools
import logging

# Configure logging to output to console (can be modified to log to a file)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_queries(func):
    """
    Decorator that logs the SQL query before executing it.
    
    Args:
        func: The function to be decorated, which executes a database query.
    
    Returns:
        wrapper: The wrapped function that logs the query and then executes it.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from the arguments or keyword arguments
        query = None
        if args and isinstance(args[0], str):
            query = args[0]
        elif 'query' in kwargs and isinstance(kwargs['query'], str):
            query = kwargs['query']
        
        if query:
            logging.info(f"Executing query: {query}")
        else:
            logging.warning("No query found in function arguments")
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise
    
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the database using the provided query.
    
    Args:
        query: The SQL query to execute.
    
    Returns:
        List of rows from the query result.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    try:
        users = fetch_all_users(query="SELECT * FROM users")
        print(users)
    except Exception as e:
        print(f"Failed to fetch users: {e}")