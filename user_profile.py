import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk

# Connect to MySQL database
def connect():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="password123",  
        database="cookbook"  
    )
    if connection.is_connected():
        print("connected!")
        return connection

def display_profile(username):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM profile WHERE username = %s", (username,))
    user = cursor.fetchall()
    if user:
        user_id= user[0][0]
        name = user[0][1]
        email= user[0][4]
        label_user_id.config(text="Username: " + str(user_id))
        label_name.config(text="Email: " + name)
        label_email.config(text="Bio: " + email)

# main root
root = tk.Tk()
root.title("User Profile")


label_user_id = tk.Label(root, text="Username: ")
label_user_id.pack()

label_email = tk.Label(root, text="Email: ")
label_email.pack()

label_name = tk.Label(root, text="Bio: ")
label_name.pack()

display_profile('nirdesh')


root.mainloop()
