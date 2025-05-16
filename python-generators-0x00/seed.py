#!/usr/bin/python3

import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, data_file):
    """Insert data from CSV file into user_data table, skipping duplicates."""
    try:
        cursor = connection.cursor()
        with open(data_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Validate UUID
                try:
                    uuid_obj = uuid.UUID(row['user_id'])
                except ValueError:
                    continue  # Skip invalid UUIDs
                # Check if user_id exists
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id = %s", (row['user_id'],))
                if cursor.fetchone()[0] == 0:
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        row['user_id'],
                        row['name'],
                        row['email'],
                        float(row['age'])
                    ))
        connection.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {data_file} not found")
