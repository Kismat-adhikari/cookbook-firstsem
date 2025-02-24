import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

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

# Create the main window
root = tk.Tk()
root.title("Simple Food Entry Form")
root.geometry("300x700")  # Increased window size to accommodate image display

# Register the validation command
vcmd_numeric = (root.register(validate_numeric_input), '%P')
vcmd_rating = (root.register(validate_rating_input), '%P')

# Create and place labels, entry fields, dropdowns, and buttons

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
submit_button = tk.Button(root, text="Submit")
submit_button.pack(pady=20)

# Fullscrean
root.state("zoomed")

# Start the main loop
root.mainloop()
