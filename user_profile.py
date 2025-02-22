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
    cursor = connection.cursor()
    print(username)
    cursor.execute("SELECT * FROM profile WHERE name = %s", (username,))
    user = cursor.fetchone()
    print(user)
    if user:
        user_id= user[0]
        name = user[1]
        email= user[4]
        label_user_id.config(text="User ID: " + str(user_id))
        label_name.config(text="Name: " + name)
        label_email.config(text="Email: " + email)

# main root
root = tk.Tk()
root.title("User Profile")


# Title Label
title_label = tk.Label(root, text="User Profile", font=("Arial", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
title_label.pack(fill="x")

# Frame for user info
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
frame.pack(pady=30, padx=20, fill="both", expand=True)

label_user_id = tk.Label(frame, text="User ID: ", font=("Arial", 16), bg="#ffffff", anchor="w")
label_user_id.pack(fill="x", pady=10)

label_name = tk.Label(frame, text="Name: ", font=("Arial", 16), bg="#ffffff", anchor="w")
label_name.pack(fill="x", pady=10)

label_email = tk.Label(frame, text="Email: ", font=("Arial", 16), bg="#ffffff", anchor="w")
label_email.pack(fill="x", pady=10)



def reload_profile():
    display_profile(str(sys.argv[1]))


# Load and resize the reload icon
reload_image = Image.open("refresh.png")  # Make sure to have reload.png in your working directory
reload_image = reload_image.resize((30, 30))  # Resize image
reload_icon = ImageTk.PhotoImage(reload_image)

# Icon button
btn_reload = tk.Button(root, image=reload_icon, command=reload_profile, bd=0, highlightthickness=0)
btn_reload.place(x=20, y=20)

display_profile(str(sys.argv[1]))
root.state("zoomed")
root.geometry('800x800')
root.mainloop()
