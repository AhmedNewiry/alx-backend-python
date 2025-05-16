#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """Fetch a page of users from user_data."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Lazily yield pages of user_data."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # No more data
            break
        yield page  # Yield page
        offset += page_size