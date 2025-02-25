import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import mysql.connector

# Validation function to ensure only numbers 1-5 are entered for rating
def validate_rating_input(P):
    if P.isdigit() and (P == "" or 1 <= int(P) <= 5):
        return True
    else:
        return False

# Validation function to ensure only numbers are entered for duration
def validate_numeric_input(P):
    if P.isdigit() or P == "":
        return True
    else:
        return False

# Function to open file dialog and select an image
def select_image():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if file_path:
        # Load the image and display it in the window
        image = Image.open(file_path)
        image = image.resize((150, 150))  # Resize image to fit in the window
        img = ImageTk.PhotoImage(image)

        # Update the image label with the selected image
        image_label.config(image=img)
        image_label.image = img  # Keep a reference to avoid garbage collection

        # store the image path
        image_label.image_path = file_path

#function to connect database
def connect_to_database():
    try:
        conn= mysql.connector.connect(
            host ="localhost",
            user = "root",
            password ="password123",
            database ="cookbook"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

#function to insert data into the profile table
def insert_data():
    name = name_entry.get()
    if not name:
        print("Name is required")
        return
    title = title_entry.get()
    description = description_entry.get()
    tags = tags_entry.get()
    duration = duration_entry.get()
    rating = rating_entry.get()
    category = category_dropdown.get()
    ingredient = ingredient_entry.get()
    image_path = image_label.image_path if hasattr(image_label,'image_path') else None

# connect to the database
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        
        # Insert the data into the profiling table
        cursor.execute('''
            INSERT INTO profile (name,title, description, tags, duration, rating, category, ingredient, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
        ''', (name,title, description, tags, duration, rating, category, ingredient, image_path))
        
        conn.commit()  # Save changes
        conn.close()   # Close the connection
        
        # Clear form fields after submission
        name_entry.delete(0,tk.END)
        title_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        tags_entry.delete(0, tk.END)
        duration_entry.delete(0, tk.END)
        rating_entry.delete(0, tk.END)
        category_dropdown.set("Select Category")
        ingredient_entry.delete(0, tk.END)
        image_label.config(image=None, text="No image selected")
        print("Data inserted successfully!")


# Create the main window
root = tk.Tk()
root.title("Simple Food Entry Form")
root.geometry("300x700")  # Increased window size to accommodate image display

# Register the validation command
vcmd_numeric = (root.register(validate_numeric_input), '%P')
vcmd_rating = (root.register(validate_rating_input), '%P')

# Create and place labels, entry fields, dropdowns, and buttons

# name
name_label = tk.Label(root, text = "Name")
name_label.pack(pady = 5)
name_entry = tk.Entry(root)
name_entry.pack(pady = 5)

# Title
title_label = tk.Label(root, text="Title:")
title_label.pack(pady=5)
title_entry = tk.Entry(root)
title_entry.pack(pady=5)

# Description
description_label = tk.Label(root, text="Description:")
description_label.pack(pady=5)
description_entry = tk.Entry(root)
description_entry.pack(pady=5)

# Tags
tags_label = tk.Label(root, text="Tags:")
tags_label.pack(pady=5)
tags_entry = tk.Entry(root)
tags_entry.pack(pady=5)

# Duration
duration_label = tk.Label(root, text="Duration (minutes):")
duration_label.pack(pady=5)
duration_entry = tk.Entry(root, validate="key", validatecommand=vcmd_numeric)
duration_entry.pack(pady=5)

# Rating (1-5)
rating_label = tk.Label(root, text="Rating (1-5):")
rating_label.pack(pady=5)
rating_entry = tk.Entry(root, validate="key", validatecommand=vcmd_rating)
rating_entry.pack(pady=5)

# Category dropdown
category_label = tk.Label(root, text="Category:")
category_label.pack(pady=5)
category_options = ["Appetizer", "Main Course", "Dessert", "Beverage", "Snack"]
category_dropdown = ttk.Combobox(root, values=category_options)
category_dropdown.set("Select Category")
category_dropdown.pack(pady=5)

# Ingredient
ingredient_label = tk.Label(root, text="Ingredient:")
ingredient_label.pack(pady=5)
ingredient_entry = tk.Entry(root)
ingredient_entry.pack(pady=5)

# Image field
image_label = tk.Label(root, text="No image selected")
image_label.pack(pady=5)
image_button = tk.Button(root, text="Select Image", command=select_image)
image_button.pack(pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", command = insert_data)
submit_button.pack(pady=20)

# Fullscrean
root.state("zoomed")

# Start the main loop
root.mainloop()
