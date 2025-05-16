#!/usr/bin/python3

import mysql.connector

def stream_user_ages():
    """Stream user ages one by one using a generator."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for age in cursor:  # Single loop to yield ages
            yield age[0]
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Error streaming ages: {e}")

def calculate_average_age():
    """Calculate average age using streamed ages."""
    total = 0
    count = 0
    for age in stream_user_ages():  # Single loop to process ages
        total += float(age)
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()