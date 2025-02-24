import tkinter as tk
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow

# Initialize the main window
root = tk.Tk()
root.title("Food Feed")
root.geometry("500x400")
root.configure(bg="#f4f4f4")

# Constants for styling
BG_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
TITLE_FONT = ("Arial", 14, "bold")
DESC_FONT = ("Arial", 10)
ICON_FONT = ("Arial", 12)
USERNAME_FONT = ("Arial", 10, "italic")

# Create the card container
card = tk.Frame(root, bg=BG_COLOR, padx=15, pady=15, relief="ridge", bd=2)
card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=350)

# Title of the food item
title_label = tk.Label(card, text="Spaghetti", font=TITLE_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
title_label.pack(anchor="w", pady=(5, 2))

# Load and display the image below the title
image = Image.open("testimage.jpeg")
image = image.resize((100, 100))  # Resize the image as needed
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(card, image=photo, bg=BG_COLOR)
image_label.pack(anchor="center", pady=(5, 10))

# Category label
category_label = tk.Label(card, text="Category: Main Course", font=DESC_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
category_label.pack(anchor="w")

# Rating label
rating_label = tk.Label(card, text="⭐ ⭐ ⭐ ⭐ ☆  (4/5)", font=ICON_FONT, fg="#FFD700", bg=BG_COLOR)
rating_label.pack(anchor="w")

# Duration label
duration_label = tk.Label(card, text="⏳ Duration: 30 min", font=ICON_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
duration_label.pack(anchor="w")

# Tags label
tags_label = tk.Label(card, text="🏷 Tags: Italian, Pasta", font=DESC_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
tags_label.pack(anchor="w")

# Description label
desc_label = tk.Label(card, text="A classic spaghetti dish with tomato sauce, garlic, olive oil, and fresh herbs. Simple, delicious, and perfect for any occasion.",
                      wraplength=400, font=DESC_FONT, fg=TEXT_COLOR, bg=BG_COLOR, justify="left")
desc_label.pack(anchor="w", pady=(5, 10))

# Uploaded by label, now inside the container
username_label = tk.Label(card, text="Uploaded by: Kathy", font=USERNAME_FONT, fg="#555", bg=BG_COLOR)
username_label.pack(anchor="w")

# Like button functionality
def toggle_like():
    if like_btn["text"] == "❤ Like":
        like_btn["text"] = "💔 Unlike"
    else:
        like_btn["text"] = "❤ Like"

# Like button
like_btn = tk.Button(card, text="❤ Like", font=ICON_FONT, fg="red", bg=BG_COLOR, bd=0, command=toggle_like)
like_btn.pack(anchor="center", pady=(5, 0))

# Fullscrean
root.state("zoomed")

# Run the Tkinter main loop
root.mainloop()
