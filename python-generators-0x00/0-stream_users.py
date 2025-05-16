#!/usr/bin/python3

import mysql.connector

def stream_users():
    """Stream rows from user_data table one by one using a generator."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:  # Single loop to yield rows
            yield row
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Error streaming users: {e}")