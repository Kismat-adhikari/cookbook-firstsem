import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import io
import os
import sys

length_data = 0

def connect():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password123",
            database="cookbook"
        )
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except Error as e:
        print(e)

def retrive_data(id):
    global length_data
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE user_id = %s", (id,))
    posts = cursor.fetchall()
    length_data = len(posts)
    return posts


# Modern color scheme
BG_DARK = "#1c1c1c"
BG_MEDIUM = "#262626"
BG_COLOR = "#ffffff"
ACCENT_COLOR = "#f46464"
TEXT_COLOR = "#ffffff"
SECONDARY_COLOR = "#65676b"
LABEL_FONT = ("Segoe UI", 12)

# Font configuration
TITLE_FONT = ("Segoe UI", 22, "bold")
SUBTITLE_FONT = ("Segoe UI", 14)
BODY_FONT = ("Segoe UI", 11)
ICON_FONT = ("Segoe UI", 12)

# Navigation functions
def open_feed():
    try:
        user_id = sys.argv[1] if len(sys.argv) > 1 else '1'  # Default to user ID 1
        root.destroy()
        os.system(f'python {os.path.join(os.path.dirname(__file__), "feed.py")} {user_id}')
    except Exception as e:
        print(f"Error opening feed: {e}")


def open_posting():
    try:
        user_id = sys.argv[1] if len(sys.argv) > 1 else '1'  # Default to user ID 1
        root.destroy()
        os.system(f'python {os.path.join(os.path.dirname(__file__), "posting.py")} {user_id}')
    except Exception as e:
        print(f"Error opening posting: {e}")


def open_profile():
    try:
        user_id = sys.argv[1] if len(sys.argv) > 1 else '1'  # Default to user ID 1
        root.destroy()
        os.system(f'python {os.path.join(os.path.dirname(__file__), "user_profile.py")} {user_id}')
    except Exception as e:
        print(f"Error opening profile: {e}")


def logout():
    try:
        root.destroy()
        os.system(f'python {os.path.join(os.path.dirname(__file__), "logintest.py")}')
    except Exception as e:
        print(f"Error logging out: {e}")


# Initialize the main window
root = tk.Tk()
root.title("Taste Tracker | Food Social Media")
root.configure(bg=BG_DARK)
root.state("zoomed")  # Make window full screen

# Navbar Frame
navbar_frame = tk.Frame(root, bg=BG_MEDIUM, height=50)
navbar_frame.pack(fill="x")
navbar_frame.pack_propagate(False)  # Prevent frame from shrinking

# Navbar Buttons
feed_btn = tk.Button(navbar_frame, text="Feed", font=LABEL_FONT, bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0, command=open_feed)
feed_btn.pack(side="left", padx=20, pady=10)

posting_btn = tk.Button(navbar_frame, text="Posting", font=LABEL_FONT, bg=BG_MEDIUM, fg=TEXT_COLOR, bd=0, command=open_posting)
posting_btn.pack(side="left", padx=20, pady=10)

profile_btn = tk.Button(navbar_frame, text="Profile", font=LABEL_FONT, bg=BG_MEDIUM, fg=TEXT_COLOR, bd=0, command=open_profile)
profile_btn.pack(side="left", padx=20, pady=10)

logout_btn = tk.Button(navbar_frame, text="Logout", font=LABEL_FONT, bg=BG_MEDIUM, fg=TEXT_COLOR, bd=0, command=logout)
logout_btn.pack(side="right", padx=20, pady=10)

# Function to create a post
def create_post(parent, title, author, description, image, category, tags, duration, ingredients, rating):

    # Create a card with better shadow effect
    post_container = tk.Frame(parent, bg=BG_DARK, padx=10, pady=10)
    post_container.pack(fill="x")
    
    main_frame = tk.Frame(post_container, bg=BG_MEDIUM, padx=0, pady=0)
    main_frame.pack(fill="x")
    
    # Add shadow effect with multiple frames for depth
    for i in range(3):
        shadow = tk.Frame(post_container, bg=f"#{20+i*10:02x}{20+i*10:02x}{20+i*10:02x}")
        shadow.place(in_=main_frame, relx=1+0.002*i, rely=1+0.002*i, 
                    anchor="se", relwidth=1, relheight=1)
    main_frame.lift()
    
    # Header with profile info
    header_frame = tk.Frame(main_frame, bg=BG_MEDIUM, pady=8, padx=10)
    header_frame.pack(fill="x")
    
    profile_frame = tk.Frame(header_frame, bg=BG_MEDIUM)
    profile_frame.pack(side="left", anchor="w")
    
    username_label = tk.Label(profile_frame, text=f"Chef {author}", font=SUBTITLE_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
    username_label.pack(anchor="w")
    time_label = tk.Label(profile_frame, text="Posted 2 hours ago", font=("Segoe UI", 9), fg="#a0a0a0", bg=BG_MEDIUM)
    time_label.pack(anchor="w")
    
    # Image with better aspect ratio and centering
    image_frame = tk.Frame(main_frame, bg=BG_MEDIUM)
    image_frame.pack(fill="x")
    
    try:
        # Try to load the actual image
        image = Image.open(io.BytesIO(image))
        image = image.resize((400, 400))
    except:
        # Create a placeholder image if file not found
        image = Image.new('RGB', (600, 337), color=(233, 233, 233))
    
    # Get window width
    window_width = 500  # Default width
    
    # Calculate appropriate height while maintaining aspect ratio
    target_width = window_width
    aspect_ratio = image.width / image.height
    target_height = int(target_width / aspect_ratio)
    
    # Resize image with high quality and proper centering
    image = image.resize((target_width, target_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    
    # Create a container to center the image
    image_container = tk.Frame(image_frame, bg=BG_MEDIUM, width=window_width, height=target_height)
    image_container.pack()
    image_container.pack_propagate(False)  # Don't shrink to image size
    
    image_label = tk.Label(image_container, image=photo, bg=BG_MEDIUM)
    image_label.image = photo  # Keep reference to prevent garbage collection
    image_label.place(relx=0.5, rely=0.5, anchor="center")  # Center image
    
    # Content section with improved layout
    content_frame = tk.Frame(main_frame, bg=BG_MEDIUM, padx=10, pady=12)
    content_frame.pack(fill="x")
    
    food_name_label = tk.Label(content_frame, text=title, font=TITLE_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
    food_name_label.pack(anchor="w")
    
    desc_label = tk.Label(content_frame, text=description, wraplength=470, font=BODY_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM, justify="left")
    desc_label.pack(anchor="w", pady=(8, 12))
    
    # Details section with better icons and organization
    details_frame = tk.Frame(content_frame, bg=BG_MEDIUM)
    details_frame.pack(fill="x", pady=5)
    
    # Left column
    left_details = tk.Frame(details_frame, bg=BG_MEDIUM)
    left_details.pack(side="left", fill="y", anchor="w")
    
    category_label = tk.Label(left_details, text=f"🍽️ {category}", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
    category_label.pack(anchor="w", pady=3)
    
    prep_label = tk.Label(left_details, text=f"⏱️ {duration} min", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
    prep_label.pack(anchor="w", pady=3)
    
    # Right column
    right_details = tk.Frame(details_frame, bg=BG_MEDIUM)
    right_details.pack(side="right", fill="y", anchor="e")
    
    rating_label = tk.Label(right_details, text=f" Rating: {rating}/5", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
    rating_label.pack(anchor="e", pady=3)
    
    servings_label = tk.Label(right_details, text="🍴 Serves: 4 people", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
    servings_label.pack(anchor="e", pady=3)
    
    # Tags with better styling
    tags_frame = tk.Frame(content_frame, bg=BG_MEDIUM)
    tags_frame.pack(fill="x", pady=(10, 0))
    
    # Create styled tag buttons
    tags = tags.split(",")
    for tag in tags:
        tag_btn = tk.Label(tags_frame, text=f"#{tag}", font=("Segoe UI", 10), 
                          fg=ACCENT_COLOR, bg=f"#ffebee", padx=8, pady=2)
        tag_btn.pack(side="left", padx=(0, 8))
    
    return main_frame

# Create a canvas and scrollbar for the posts
canvas = tk.Canvas(root, bg=BG_DARK)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_DARK)

# Configure the canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# enable mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Get the posts from the database
posts = retrive_data(1)
print(len(posts))
for post in posts:
    post_id, name, detail, image, category, tags, duration, ingredient, rating, user_id = post
    # Create posts inside the scrollable frame
    post_frame = create_post(scrollable_frame, name, user_id, detail, image, category, tags, duration, ingredient, rating)
    post_frame.pack(fill="x", pady=10)
    


# Run the Tkinter main loop
root.mainloop()