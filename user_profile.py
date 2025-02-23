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
        cursor.execute("SELECT id,username,name,age,phone_number,email,cooktype,experience FROM profile WHERE name = %s", (username,))
        user = cursor.fetchone()
        print(user)
        if user:
            user_id= user[0]
            full_name = user[1]
            username = user[2]
            age = user[3]
            phone_number= user[4]
            email= user[5]
            cooking_type = user[6]
            experience = user[7]

            label_user_id.config(text="User ID: " +str(user_id))
            label_user_id.config(text="Username: " + str(username))
            label_name.config(text="Name: " + full_name)
            label_email.config(text="Email: " + email)
            label_age.config(text="Age: " + str(age))
            label_phone_number.config(text="Phone: " + phone_number)
            label_cooking_type.config(text="Cook Type: " + str(cooking_type))
            label_experience.config(text="Experience: " + experience)

    except Error as e:
        print(f"Error :{e}")
        messagebox.showerror("Error", "Could not load profile Information.")

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

# scrollbar 
canvas = tk.Canvas(root)
canvas.pack(side="left",fill="both",expand= True)

scrollbar = tk.Scrollbar(root,orient="vertical",command=canvas.yview)
scrollbar.pack(side="right",fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Frame for user info
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
frame.pack(pady=30, padx=20, fill="both", expand=True)

label_user_id = tk.Label(frame, text="Username: ", font=("Helvetica", 16), bg="#ffffff", anchor="center",width=30)
label_user_id.pack(fill="x", pady=10)

label_name = tk.Label(frame, text="Name: ", font=("Helvetica", 16), bg="#ffffff", anchor="center",width=30)
label_name.pack(fill="x", pady=10)

label_email = tk.Label(frame, text="Email: ", font=("Arial", 16), bg="#ffffff", anchor="center",width=30)
label_email.pack(fill="x", pady=10)

label_age = tk.Label(frame, text="Age: ", font=("Helvetica", 16), bg="#ffffff", anchor="center",width=30)
label_age.pack(fill="x", pady=10)

label_phone_number = tk.Label(frame, text="Phone: ", font=("Helvetica", 16), bg="#ffffff", anchor="center",width=30)
label_phone_number.pack(fill="x", pady=10)

label_cooking_type = tk.Label(frame, text="Cook Type: ", font=("Helvetica", 16), bg="#ffffff", anchor="center",width=30)
label_cooking_type.pack(fill="x", pady=10)

label_experience = tk.Label(frame, text="Experience: ", font=("Helvetica", 16), bg="#ffffff", anchor="center",width=30)
label_experience.pack(fill="x", pady=10)



def reload_profile():
    display_profile(str(sys.argv[1]))

reload_button = tk.Button(root, text="Reload Profile", font=("Arial", 14), bg="#00796b", fg="white", command=reload_profile)
reload_button.pack(pady=10)

# display_profile(str(sys.argv[1]))
display_profile("nirdesh")

#  updating canvas scroll
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))
canvas.update_idletasks()

root.state("zoomed")
root.geometry('800x800')

root.mainloop()


