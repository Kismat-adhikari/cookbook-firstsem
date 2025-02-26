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
            age = user[6]
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
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error :{e}")
        messagebox.showerror("Error", "Could not load profile Information.")

def display_posts(id):

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

    def retrive_data(id):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts WHERE user_id = %s", (id,))
        posts = cursor.fetchall()
        return posts

    def create_post(parent, title, author, description, image, category, tags, duration, ingredients, rating):

        # To get username
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(f"SELECT username FROM profile WHERE id={author}")
        author = cursor.fetchone()[0]

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

        # Ingredients section with better layout
        ingredients_frame = tk.Frame(main_frame, bg=BG_MEDIUM, padx=10, pady=12)
        ingredients_frame.pack(fill="x")
        ingredients_label = tk.Label(ingredients_frame, text=f"Ingredients:\n{ingredient}", font=SUBTITLE_FONT, fg=TEXT_COLOR, bg=BG_MEDIUM)
        ingredients_label.pack(anchor="w")
        
        return main_frame


    posts = retrive_data(id)
    for post in posts:
        post_id, name, detail, image, category, tags, duration, ingredient, rating, user_id = post
        # Create posts inside the scrollable frame
        # Posts frame with improved styling
        posts_frame = tk.Frame(scrollable_frame, bg="#262626", padx=30, pady=30, relief="flat")
        posts_frame.pack(fill="x", expand=True, padx=20, pady=10)

        posts_label = tk.Label(posts_frame, text="User Posts", font=("Segoe UI", 16, "bold"), bg="#262626", fg="#f46464", anchor="w")
        posts_label.pack(pady=(0, 20), anchor="w")

        create_post(posts_frame, name, user_id, detail, image, category, tags, duration, ingredient, rating)


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




# Enable mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

print(sys.argv[1])
display_profile(str(sys.argv[1]))
display_posts(main_id)

root.state("zoomed")
root.mainloop()