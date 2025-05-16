#!/usr/bin/python3

import mysql.connector

def stream_users_in_batches(batch_size):
    """Fetch rows from user_data in batches using a generator."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
    except mysql.connector.Error as e:
        print(f"Error streaming batches: {e}")
        return  # Return on connection failure
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)  # Fetch batch
            if not rows:  # No more rows
                break
            yield rows  # Yield batch
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Error streaming batches: {e}")
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    """Yield users over 25 from batches."""
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if user['age'] > 25:
                yield user  # Yield filtered user