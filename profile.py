
# function to fetch and display profile
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="password123",  
    database="cookbook"  
)

cursor = db.cursor()

def display_profile(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if user:
        user_id, username, email, bio, profile_pic = user
        
        
        label_username.config(text="Username: " + username)
        label_email.config(text="Email: " + email)
        label_bio.config(text="Bio: " + bio)
        label_profile_pic.config(text="Profile Picture: " + profile_pic)  
        try:
            
            image = Image.open(profile_pic)
            image = image.resize((100, 100))  
            profile_img = ImageTk.PhotoImage(image)
            
            
            label_image.config(image=profile_img)
            label_image.image = profile_img  
        except Exception as e:
            print("Error loading image:", e)
            label_image.config(text="No image available")
    else:
        messagebox.showerror("Error", "User not found!")

# main window
window = tk.Tk()
window.title("User Profile")


label_username = tk.Label(window, text="Username: ")
label_username.pack()

label_email = tk.Label(window, text="Email: ")
label_email.pack()

label_bio = tk.Label(window, text="Bio: ")
label_bio.pack()

label_profile_pic = tk.Label(window, text="Profile Picture: ")
label_profile_pic.pack()


label_image = tk.Label(window)
label_image.pack()

display_profile('shreya')


window.mainloop()
