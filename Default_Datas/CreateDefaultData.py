#this program should only be ran once to create database and tables.
import mysql.connector
from mysql.connector import Error   

def connection_create():
    try:
        connection=mysql.connector.connect(
            host='localhost',      
            user='root',    
            password='password123' 
            )
        if connection.is_connected():   
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS cookbook")
            cursor.execute("USE cookbook")
            cursor.execute("DROP TABLE IF EXISTS posts")
            cursor.execute("DROP TABLE IF EXISTS profile")
            cursor.execute('''CREATE TABLE IF NOT EXISTS profile (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            username VARCHAR(50) NOT NULL,
                            password VARCHAR(300) NOT NULL,
                            phone_number VARCHAR(15),
                            email VARCHAR(100) NOT NULL,
                            age INT NOT NULL,
                            cook_type VARCHAR(50),
                            experience VARCHAR(50),
                            profile_pic LONGBLOB,
                            bio TEXT
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            detail TEXT,
                            image LONGBLOB,
                            category VARCHAR(50),
                            tags VARCHAR(100),
                            duration VARCHAR(50),
                            ingredient TEXT,
                            rating INT,
                            user_id INT,
                            FOREIGN KEY (user_id) REFERENCES profile(id)
                            )''')
    except Error as e:
        print("ERROR: \n", e)   
connection_create()