import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

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

def switch_to_signup():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Full Name
    tk.Label(main_frame, text="Full Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    fullname_entry = tk.Entry(main_frame)
    fullname_entry.grid(row=0, column=1, padx=10, pady=10)
    print(fullname_entry)

    # Username
    tk.Label(main_frame, text="Username", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    username_entry = tk.Entry(main_frame)
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    # Age (number only)
    tk.Label(main_frame, text="Age", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    age_entry = tk.Entry(main_frame)
    age_entry.grid(row=2, column=1, padx=10, pady=10)

    # Phone number (number only)
    tk.Label(main_frame, text="Phone", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    phone_entry = tk.Entry(main_frame)
    phone_entry.grid(row=3, column=1, padx=10, pady=10)

    # Experience (dropdown - number only)
    tk.Label(main_frame, text="Experience (years)", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    experience = tk.StringVar(main_frame)
    experience_dropdown = ttk.Combobox(main_frame, textvariable=experience, state="readonly")
    experience_dropdown['values'] = [str(i) for i in range(1, 51)]  # Up to 50 years experience
    experience_dropdown.grid(row=4, column=1, padx=10, pady=10)

    # Cook Type (dropdown)
    tk.Label(main_frame, text="Cook Type", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=10, sticky="w")
    cook_type = tk.StringVar(main_frame)
    cook_type_dropdown = ttk.Combobox(main_frame, textvariable=cook_type, state="readonly")
    cook_type_dropdown['values'] = ['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Dessert Specialist']
    cook_type_dropdown.grid(row=5, column=1, padx=10, pady=10)

    # Password
    tk.Label(main_frame, text="Password", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=10, sticky="w")
    password_entry = tk.Entry(main_frame, show="*")
    password_entry.grid(row=6, column=1, padx=10, pady=10)

    # Confirm Password
    tk.Label(main_frame, text="Confirm Password", font=("Arial", 12)).grid(row=7, column=0, padx=10, pady=10, sticky="w")
    confirm_password_entry = tk.Entry(main_frame, show="*")
    confirm_password_entry.grid(row=7, column=1, padx=10, pady=10)

    # Signup button
    signup_button = tk.Button(main_frame, text="Sign Up", font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
    signup_button.grid(row=8, columnspan=2, pady=20)

    # Switch to Login button
    switch_to_login_button = tk.Button(main_frame, text="Back to Login", font=("Arial", 10), command=switch_to_login)
    switch_to_login_button.grid(row=9, columnspan=2, pady=5)

def switch_to_login():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Centering content
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    # Username or Email
    tk.Label(main_frame, text="Username or Email", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    username_email_entry = tk.Entry(main_frame)
    username_email_entry.grid(row=1, column=1, padx=10, pady=10)

    # Password
    tk.Label(main_frame, text="Password", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(main_frame, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    # Login button
    login_button = tk.Button(main_frame, text="Login", font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
    login_button.grid(row=3, columnspan=2, pady=20)

    # Switch to Signup button
    signup_button = tk.Button(main_frame, text="Sign Up", font=("Arial", 10), command=switch_to_signup)
    signup_button.grid(row=4, columnspan=2, pady=5)

# Main window setup
root = tk.Tk()
root.title("Login and Signup")

# Set window size to fit both forms perfectly
root.geometry("400x500")  # Adjusted size

main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Start with the login screen
switch_to_login()

root.mainloop()
