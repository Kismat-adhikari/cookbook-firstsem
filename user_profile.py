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

# inserting new user data into database
def insert_user(username,email,bio,profile_pic,full_name,cooking_type,experience):
    try:
        query=""" 
        INSERT INTO profile (username,email,bio,profile_pic,full_name,cooking_type,experience)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """

        connection= connect()
        cursor=connection.cursor()

        data=(username,email,bio,profile_pic,full_name,cooking_type,experience)
        
        cursor.execute(query,data)

        connection.commit()

        messagebox.showinfo("success","user data inserted successfully!!")

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error",f"Failed to insert data{e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def display_profile(username):
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM profile WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            user_id= user[0]
            full_name = user[4]
            email= user[2]
            bio = user [3]
            profile_pic = user[5]
            cooking_type = user[6]
            experience = user[7]

            label_user_id.config(text="Username: " + str(user_id))
            label_name.config(text="Name: " + full_name)
            label_email.config(text="Email: " + email)

            if profile_pic:
                img= Image.open(profile_pic)
                img= img.resize((100,100))
                profile_pic_image = ImageTk.PhotoImage(img)
                profile_pic_label.config(image=profile_pic_image)
                profile_pic_label.image=profile_pic_image
            else:
                profile_pic_label.config(image=" ",text="No profile picture")
        else:
            messagebox.showerror("Error","user not found!")

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
    display_profile('nirdesh')

reload_button = tk.Button(root, text="Reload Profile", font=("Arial", 14), bg="#00796b", fg="white", command=reload_profile)
reload_button.pack(pady=10)



display_profile('nirdesh')

<<<<<<< HEAD
# Main event loop
=======
display_profile(str(sys.argv[1]))
root.state("zoomed")
root.geometry('800x800')
>>>>>>> c1c1d03812626bc01d1ab47540b572cc98bbd648
root.mainloop()


