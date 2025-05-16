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

def batch_processing(batch_size):
    """Process batches to filter users over 25."""
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if user['age'] > 25:
                print(user)