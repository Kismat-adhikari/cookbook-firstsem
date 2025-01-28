import mysql.connector
def connect():
        try:
            connection = mysql.connector.connect(
                host='localhost',  
                user='root',       
                password='password123'  
                )  
            if connection.is_connected():
                print("Successfully connected to the database")
                cursor = connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS cookbook")
                cursor.execute("USE cookbook")
                cursor.execute("CREATE TABLE IF NOT EXISTS profile (id INT AUTO_INCREMENT PRIMARY KEY, name varchar(225),tag varchar(225), email varchar(255), phone varchar(255), experience varchar(50), cook_type varchar(50), password varchar(500));")
                print("Database 'cookbook' created successfully!")
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
connect()