import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import sys

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
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM profile WHERE name = %s", (username,))
        user = cursor.fetchone()
        print(user)
        if user:
            user_id= user[0]
            username = user[2]
            full_name = user[1]
            email= user[5]
            age = user[3]
            cooking_type = user[6]
            experience = user[7]

            label_user_id.config(text="" + str(username))
            label_name.config(text="Name: " + full_name)
            label_email.config(text="Email: " + email)
    except Error as e:
        print(f"Error :{e}")
        messagebox.show

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# main root
root = tk.Tk()
root.title("User Profile")
root.config(bg="#f5f5f5")


# Title Label
title_label = tk.Label(root, text="User Profile", font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
title_label.pack(fill="x")

# Frame for user info
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
frame.pack(pady=30, padx=20, fill="both", expand=True)

label_user_id = tk.Label(frame, text="Username: ", font=("Helvetica", 16), bg="#ffffff", anchor="w")
label_user_id.pack(fill="x", pady=10)

label_name = tk.Label(frame, text="Name: ", font=("Helvetica", 16), bg="#ffffff", anchor="w")
label_name.pack(fill="x", pady=10)

label_email = tk.Label(frame, text="Email: ", font=("Arial", 16), bg="#ffffff", anchor="w")
label_email.pack(fill="x", pady=10)



def reload_profile():
    display_profile(str(sys.argv[1]))

reload_button = tk.Button(root, text="Reload Profile", font=("Arial", 14), bg="#00796b", fg="white", command=reload_profile)
reload_button.pack(pady=10)

# display_profile(str(sys.argv[1]))
display_profile("nirdesh")
root.state("zoomed")
root.geometry('800x800')

root.mainloop()


