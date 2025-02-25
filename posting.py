import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector

image_data = None

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
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;.jpeg;.gif")])
    if file_path:
        global image_data
        try:
            with open(file_path, 'rb') as file:
                image_data = file.read()
            
            # Load the original image
            original_image = Image.open(file_path)
            
            # Resize to a much larger size - 40x40pixels
            image = original_image.resize((40, 40))
            
            img_tk = ImageTk.PhotoImage(image)
            
            # Update the label with the new image
            image_label.config(image=img_tk)
            image_label.image = img_tk  # Keep a reference to prevent garbage collection
            
            # Reset width and height to accommodate the image
            image_label.config(width=40, height=40)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read image: {e}")

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
    description = description_entry.get("1.0", tk.END).strip()
    tags = tags_entry.get()
    duration = duration_entry.get()
    rating = rating_entry.get()
    category = category_dropdown.get()
    ingredient = ingredient_entry.get("1.0", tk.END).strip()
    image_path = image_label.image_path if hasattr(image_label,'image_path') else None

# connect to the database
    conn = connect_to_database()
    if conn:
        global image_data
        cursor = conn.cursor()
        
        # Insert the data into the profiling table
        cursor.execute('''use cookbook''')
        cursor.execute('''
            INSERT INTO posts (name, detail, tags, duration, rating, category, ingredient, image, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
        ''', (name, description, tags, duration, rating, category, ingredient, image_data, 1))
        print("Data inserted successfully")
        conn.commit()  # Save changes
        conn.close()   # Close the connection


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

# Description
description_label = tk.Label(root, text="Description:")
description_label.pack(pady=5)
description_entry = tk.Text(root,height=5)
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
ingredient_entry = tk.Text(root, height=2)
ingredient_entry.pack(pady=5)

# Image field
image_label = tk.Label(root, text="No image selected")
image_label.pack(pady=5)
image_button = tk.Button(root, text="Select Image", command=upload_image)
image_button.pack(pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", command = insert_data)
submit_button.pack(pady=20)

# Fullscrean
root.state("zoomed")

# Start the main loop
root.mainloop()
