import mysql.connector
from mysql.connector import Error


connection=mysql.connector.connect(
    host='localhost',
    database='cookbook',      
    user='root', 
    password='password123' 
)

c = connection.cursor()
c.execute("SELECT * FROM profiling")
r = c.fetchall()
for row in r:
    print(row)


if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")
print("hello")
print("world")