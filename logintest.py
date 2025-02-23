import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import mysql.connector
from mysql.connector import Error
import PIL
from PIL import Image, ImageTk
#import os to connect to other files
import os 

image_data = None
# Connect to MySQL  
def connect():
    try:
        connection=mysql.connector.connect(
            host='localhost',
            database='cookbook',      
            user='root', 
            password='password123' 
            )
        if connection.is_connected():
            print("connected!")
            return connection
    except Error as e:
        print("ERROR: \n", e)

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        try:
            global image_data
            with open(file_path, 'rb') as file:
                image_data = file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read image: {e}")
        image = Image.open(file_path).resize((200, 200))
        img_tk = ImageTk.PhotoImage(image)
        label_image.config(image=img_tk)
        label_image.image = img_tk 

def store_data(fullname_entry,username_entry, email_entry,age_entry,phone_entry,experience,cook_type,password_entry):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO profile (name, username, email, age, phone_number, experience, cook_type, password, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (fullname_entry.get(), username_entry.get(), email_entry.get(), age_entry.get(), phone_entry.get(), experience.get(), cook_type.get(), password_entry.get(), image_data))
    connection.commit()
    connection.close()
    name=fullname_entry.get()
    root.destroy() 
    goto_profile(name)
    
def goto_profile(name):
    os.system(f'python user_profile.py {name}')

def check_login(username_email_entry, password_entry):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT name, password FROM profile WHERE username = %s OR email = %s", (username_email_entry.get(), username_email_entry.get()))
    user = cursor.fetchone()
    if user:
        name, password = user
        if password == password_entry.get():
            root.destroy()
            goto_profile(name)
        else:
            messagebox.showerror("Error", "Invalid Password")
    else:
        messagebox.showerror("Error", "User not found")

def switch_to_signup():
    global main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    main_frame.configure(bg="#f7f7f7")

    # Add Scrollbar
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Title
    tk.Label(scrollable_frame, text="Sign Up", font=("Arial", 24, "bold"), bg="#f7f7f7").grid(row=0, columnspan=2, pady=20)

    # Form Fields
    fields = ["Full Name", "Username", "Email", "Age", "Phone", "Password", "Confirm Password"]
    entries = []
    for i, field in enumerate(fields):
        tk.Label(scrollable_frame, text=field, font=("Arial", 14), bg="#f7f7f7").grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(scrollable_frame, font=("Arial", 14), width=30)
        entry.grid(row=i + 1, column=1, padx=10, pady=5)
        entries.append(entry)

    fullname_entry, username_entry, email_entry, age_entry, phone_entry, password_entry, confirm_password_entry = entries

    # Dropdowns
    tk.Label(scrollable_frame, text="Experience (years)", font=("Arial", 14), bg="#f7f7f7").grid(row=8, column=0, sticky="w", padx=10, pady=5)
    experience = ttk.Combobox(scrollable_frame, values=[str(i) for i in range(1, 51)], state="readonly", width=28)
    experience.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(scrollable_frame, text="Cook Type", font=("Arial", 14), bg="#f7f7f7").grid(row=9, column=0, sticky="w", padx=10, pady=5)
    cook_type = ttk.Combobox(scrollable_frame, values=["Vegetarian", "Non-Vegetarian", "Vegan", "Dessert Specialist"], state="readonly", width=28)
    cook_type.grid(row=9, column=1, padx=10, pady=5)

    # Upload Image Button
    upload_photo_button = tk.Button(scrollable_frame, text="Upload Profile Picture", command=upload_image, bg="#4CAF50", fg="white", font=("Arial", 14), relief="flat")
    upload_photo_button.grid(row=10, columnspan=2, pady=10)

    global label_image
    label_image = tk.Label(scrollable_frame, bg="#f7f7f7")
    label_image.grid(row=11, columnspan=2, pady=10)

    # Signup Button
    signup_button = tk.Button(scrollable_frame, text="Sign Up", command=lambda: store_data(fullname_entry, username_entry, email_entry, age_entry, phone_entry, experience, cook_type, password_entry),
                              bg="#4CAF50", fg="white", font=("Arial", 16, "bold"), relief="flat", width=20)
    signup_button.grid(row=12, columnspan=2, pady=20)

    # Switch to Login Button
    switch_to_login_button = tk.Button(scrollable_frame, text="Back to Login", command=switch_to_login, bg="#cccccc", font=("Arial", 12), relief="flat")
    switch_to_login_button.grid(row=13, columnspan=2, pady=5)

def switch_to_login():
    for widget in main_frame.winfo_children():
        widget.destroy()

    main_frame.configure(bg="#f7f7f7")

    # Title
    tk.Label(main_frame, text="Login", font=("Arial", 24, "bold"), bg="#f7f7f7").grid(row=0, columnspan=2, pady=20)

    # Username/Email
    tk.Label(main_frame, text="Username or Email", font=("Arial", 14), bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=10)
    username_email_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
    username_email_entry.grid(row=1, column=1, padx=10, pady=10)

    # Password
    tk.Label(main_frame, text="Password", font=("Arial", 14), bg="#f7f7f7").grid(row=2, column=0, padx=10, pady=10)
    password_entry = tk.Entry(main_frame, show="*", font=("Arial", 14), width=30)
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    # Login Button
    login_button = tk.Button(main_frame, text="Login", command=lambda: check_login(username_email_entry,password_entry), bg="#4CAF50", fg="white", font=("Arial", 16, "bold"), relief="flat", width=20)
    login_button.grid(row=3, columnspan=2, pady=20)

    # Switch to Signup Button
    signup_button = tk.Button(main_frame, text="Sign Up", command=switch_to_signup, bg="#cccccc", font=("Arial", 12), relief="flat")
    signup_button.grid(row=4, columnspan=2, pady=5)

# Main window setup
root = tk.Tk()
root.title("Login and Signup")

# Set window size to fit both forms perfectly
root.state("zoomed")  # Fullscreen
root.geometry("400x600")  # Adjusted size

main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Start with the login screen
switch_to_login()

root.mainloop()
