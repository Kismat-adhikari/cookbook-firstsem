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
            cursor.execute('''CREATE TABLE IF NOT EXISTS profile (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            username VARCHAR(50) NOT NULL,
                            password VARCHAR(50) NOT NULL,
                            birth_date DATE,
                            phone_number VARCHAR(15),
                            email VARCHAR(100) NOT NULL,
                            age INT NOT NULL,
                            cook_type VARCHAR(50),
                            experience TEXT)''')
    except Error as e:
        print("ERROR: \n", e)   
connection_create()