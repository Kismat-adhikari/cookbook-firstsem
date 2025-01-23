
from datetime import datetime
import mysql.connector

c=mysql.connector.connect(
    host='localhost',
    database='cookbook',      
    user='root', 
    password='password123' 
)
 
cursor = c.cursor()
sql = """
INSERT INTO profiling (first_name, last_name, birth_date, phone_number, email, age, qualifications)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
first_name = 'John'
last_name = 'Cina'
birth_date = datetime.strptime('20/12/2015', '%d/%m/%Y').date()  # Convert string to date object
phone_number = '9848328846'  # Store as a string to prevent overflow
email = '123@gmail.com'
age = 18
qualification = 'Software Engineer'
values = (first_name, last_name, birth_date, phone_number, email, age, qualification)
cursor.execute(sql, values)
c.commit()
cursor.close()
c.close()