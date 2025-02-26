import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk, ImageDraw, ImageOps
import sys
import io
import os

main_id = None

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
    
def display_profile(id):
    connection = connect()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM profile WHERE id = %s", (id,))
        user = cursor.fetchone()
        if user:
            # Extract the user data
            user_id= user[0]
            full_name = user[1]
            username = user[2]
            age = user[3]
            phone_number= user[4]
            email= user[5]
            cooking_type = user[7]
            experience = user[8]
            profilePic = user[9]
            bio = user[10]

            # asgining main_id
            global main_id
            main_id = user_id

            # Improved profile picture processing
            image = Image.open(io.BytesIO(profilePic)).convert("RGBA")
            
            # Resize image to a square while maintaining aspect ratio
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Create a new square background
            background = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
            
            # Calculate position to center the image
            offset = ((300 - image.width) // 2, (300 - image.height) // 2)
            
            # Paste the image onto the background
            background.paste(image, offset, image)

            # Create circular mask
            mask = Image.new("L", (300, 300), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 300, 300), fill=255)

            # Apply mask to create circular image
            output = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
            output.paste(background, (0, 0), mask)

            # Add a border
            border_color = (244, 100, 100, 255)  # Reddish border
            border_width = 10
            bordered_image = Image.new("RGBA", (320, 320), border_color)
            bordered_image.paste(output, ((border_width, border_width)), output)

            img_tk = ImageTk.PhotoImage(bordered_image)
            label_image.config(image=img_tk)
            label_image.image = img_tk
            
            #label the vaiables and config data
            label_user_id.config(text="Username: " +str(username))
            label_name.config(text="Name: " + full_name)
            label_email.config(text="Email: " + email)
            label_age.config(text="Age: " + str(age))
            label_phone_number.config(text="Phone: " + phone_number)
            label_cooking_type.config(text="Cook Type: " + str(cooking_type))
            label_experience.config(text="Experience: " + str(experience))
            label_bio.config(text="Bio: "+ str(bio))
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error :{e}")
        messagebox.showerror("Error", "Could not load profile Information.")

def display_posts(id):
    connection = connect()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts WHERE user_id = %s", (id,))
        posts = cursor.fetchall()
        
        for post in posts:
            # Create the card container with improved styling
            card = tk.Frame(posts_frame, bg="#1c1c1c", padx=20, pady=20, relief="raised", bd=1)
            card.pack(fill="x", pady=10)

            # Title of the food item
            title_label = tk.Label(card, text=post[0], font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1c1c1c")
            title_label.pack(anchor="w", pady=(0, 10))

            # Load and display the image from the database
            try:
                post_image = Image.open(io.BytesIO(post[2])).convert("RGBA")
                post_image = post_image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(post_image)
                image_label = tk.Label(card, image=photo, bg="#1c1c1c")
                image_label.image = photo  # Keep a reference
                image_label.pack(anchor="center", pady=(0, 10))
            except Exception as e:
                print(f"Error loading image: {e}")
                # Display a placeholder image if the image cannot be loaded
                placeholder = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
                photo = ImageTk.PhotoImage(placeholder)
                image_label = tk.Label(card, image=photo, bg="#1c1c1c")
                image_label.image = photo
                image_label.pack(anchor="center", pady=(0, 10))

            # Additional details in a more organized layout
            details_frame = tk.Frame(card, bg="#1c1c1c")
            details_frame.pack(fill="x", pady=(0, 10))

            category_label = tk.Label(details_frame, text="Category: Main Course", font=("Segoe UI", 12), fg="#ffffff", bg="#1c1c1c")
            category_label.pack(anchor="w")

            rating_label = tk.Label(details_frame, text="⭐ ⭐ ⭐ ⭐ ☆  (4/5)", font=("Segoe UI", 12), fg="#FFD700", bg="#1c1c1c")
            rating_label.pack(anchor="w")

            duration_label = tk.Label(details_frame, text="⏳ Duration: 30 min", font=("Segoe UI", 12), fg="#ffffff", bg="#1c1c1c")
            duration_label.pack(anchor="w")

            tags_label = tk.Label(details_frame, text="🏷 Tags: Italian, Pasta", font=("Segoe UI", 12), fg="#ffffff", bg="#1c1c1c")
            tags_label.pack(anchor="w")

            desc_label = tk.Label(card, text="A classic spaghetti dish with tomato sauce, garlic, olive oil, and fresh herbs. Simple, delicious, and perfect for any occasion.",
                                wraplength=500, font=("Segoe UI", 12), fg="#ffffff", bg="#1c1c1c", justify="left")
            desc_label.pack(anchor="w", pady=(10, 0))

    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Could not load profile Information.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Navbar function
def open_feed():
    root.destroy()
    os.system(f'python {os.path.join(os.path.dirname(__file__), "feed.py")} {main_id}')

def open_posting():
    root.destroy()
    os.system(f'python {os.path.join(os.path.dirname(__file__), "posting.py")} {main_id}')

def logout():
    root.destroy()
    os.system(f'python {os.path.join(os.path.dirname(__file__), "logintest.py")}')

# main root
root = tk.Tk()
root.title("User Profile")
root.config(bg="#1c1c1c")

# Navbar Frame
navbar_frame = tk.Frame(root, bg="#262626", height=50)
navbar_frame.pack(fill="x")
navbar_frame.pack_propagate(False)  # Prevent frame from shrinking

# Navbar Buttons
feed_btn = tk.Button(navbar_frame, text="Feed", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", bd=0, command=open_feed)
feed_btn.pack(side="left", padx=20, pady=10)

posting_btn = tk.Button(navbar_frame, text="Posting", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", bd=0, command=open_posting)
posting_btn.pack(side="left", padx=20, pady=10)

profile_btn = tk.Button(navbar_frame, text="Profile", font=("Segoe UI", 12), bg="#f46464", fg="#ffffff", bd=0)
profile_btn.pack(side="left", padx=20, pady=10)

logout_btn = tk.Button(navbar_frame, text="Logout", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", bd=0, command=logout)
logout_btn.pack(side="right", padx=20, pady=10)

# Main Frame with improved padding
main_frame = tk.Frame(root, bg="#1c1c1c", padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# Title Label with more padding and centered
title_label = tk.Label(main_frame, text="User Profile", font=("Segoe UI", 24, "bold"), bg="#f46464", fg="#ffffff", padx=20, pady=15)
title_label.pack(fill="x", pady=(0, 20))

# Create a canvas with scrollbar for scrolling
canvas = tk.Canvas(main_frame, bg="#1c1c1c", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

# Configure the scrollable frame
scrollable_frame = tk.Frame(canvas, bg="#1c1c1c")
scrollable_frame.bind(
    "<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Create a window inside the canvas to hold the scrollable frame
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Frame for user info with improved styling
user_info_frame = tk.Frame(scrollable_frame, bg="#262626", padx=30, pady=30, relief="flat")
user_info_frame.pack(fill="x", expand=True, padx=20, pady=10)

# Configure grid weights to make the details column wider
user_info_frame.columnconfigure(0, weight=1)  # Profile picture column
user_info_frame.columnconfigure(1, weight=3)  # User details column

# Profile picture with border
label_image = tk.Label(user_info_frame, bg="#1c1c1c", relief="solid", bd=2)
label_image.grid(row=0, column=0, rowspan=8, padx=(0, 30), sticky="nsew")

# User info labels with improved alignment and styling
label_user_id = tk.Label(user_info_frame, text="Username: ", font=("Segoe UI", 16, "bold"), bg="#262626", fg="#ffffff", anchor="w")
label_user_id.grid(row=0, column=1, pady=5, sticky="w", padx=(20, 0))

label_name = tk.Label(user_info_frame, text="Name: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_name.grid(row=1, column=1, pady=5, sticky="w", padx=(20, 0))

label_email = tk.Label(user_info_frame, text="Email: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_email.grid(row=2, column=1, pady=5, sticky="w", padx=(20, 0))

label_age = tk.Label(user_info_frame, text="Age: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_age.grid(row=3, column=1, pady=5, sticky="w", padx=(20, 0))

label_phone_number = tk.Label(user_info_frame, text="Phone: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_phone_number.grid(row=4, column=1, pady=5, sticky="w", padx=(20, 0))

label_cooking_type = tk.Label(user_info_frame, text="Cook Type: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_cooking_type.grid(row=5, column=1, pady=5, sticky="w", padx=(20, 0))

label_experience = tk.Label(user_info_frame, text="Experience: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_experience.grid(row=6, column=1, pady=5, sticky="w", padx=(20, 0))

label_bio = tk.Label(user_info_frame, text="Bio: ", font=("Segoe UI", 12), bg="#262626", fg="#ffffff", anchor="w")
label_bio.grid(row=7, column=1, pady=5, sticky="w", padx=(20, 0))

# Posts frame with improved styling
posts_frame = tk.Frame(scrollable_frame, bg="#262626", padx=30, pady=30, relief="flat")
posts_frame.pack(fill="x", expand=True, padx=20, pady=10)

posts_label = tk.Label(posts_frame, text="User Posts", font=("Segoe UI", 16, "bold"), bg="#262626", fg="#f46464", anchor="w")
posts_label.pack(pady=(0, 20), anchor="w")

# Enable mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

print(sys.argv[1])
display_profile(str(sys.argv[1]))
display_posts(main_id)

root.state("zoomed")
root.mainloop()