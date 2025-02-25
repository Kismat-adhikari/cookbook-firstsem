import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk, ImageDraw, ImageOps
import sys
import io

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

            # to make profile image a circular with border(designs)
            image = Image.open(io.BytesIO(profilePic)).convert("RGBA")
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)

            mask = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)

            image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
            image.putalpha(mask)

            border_size = 10
            border_image = Image.new("RGBA", (image.size[0] + border_size, image.size[1] + border_size), (244, 100, 100, 255))
            border_image.paste(image, (border_size // 2, border_size // 2), image)

            img_tk = ImageTk.PhotoImage(border_image)
            label_image.config(image=img_tk)
            label_image.image = img_tk
            
            #label the vaiables and config data
            label_user_id.config(text="User ID: " +str(user_id))
            label_user_id.config(text="Username: " + str(username))
            label_name.config(text="Name: " + full_name)
            label_email.config(text="Email: " + email)
            label_age.config(text="Age: " + str(age))
            label_phone_number.config(text="Phone: " + phone_number)
            label_cooking_type.config(text="Cook Type: " + str(cooking_type))
            label_experience.config(text="Experience: " + str(experience))
            label_bio.config(text="bio: "+ str(bio))
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
                print(post)
        for post in posts:
            # Create the card container
            card = tk.Frame(frame, bg=BG_COLOR, padx=15, pady=15, relief="ridge", bd=2)
            card.grid(row=1, column=0, pady=5)

            # Title of the food item
            title_label = tk.Label(card, text=post[0], font=TITLE_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
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
            username_label = tk.Label(card, text="Uploaded by: Kathy", font=USERNAME_FONT, fg="#f46464", bg=BG_COLOR)
            username_label.pack(anchor="w")

            # Like button functionality
            def toggle_like():
                if like_btn["text"] == "❤ Like":
                    like_btn["text"] = "💔 Unlike"
                else:
                    like_btn["text"] = "❤ Like"

            # Like button
            like_btn = tk.Button(card, text="❤ Like", font=ICON_FONT, fg="#f46464", bg=BG_COLOR, bd=0, command=toggle_like)
            like_btn.pack(anchor="center", pady=(5, 0))
    except Error as e:
        print(f"Error :{e}")
        messagebox.showerror("Error", "Could not load profile Information.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# main root
root = tk.Tk()
root.title("User Profile")
root.config(bg="#1c1c1c")

# Main Frame
main_frame = tk.Frame(root, bg="#1c1c1c")
main_frame.pack(expand=True, fill="both")

# Title Label
title_label = tk.Label(main_frame, text="User Profile", font=("Helvetica", 24, "bold"), bg="#f46464", fg="white", padx=10, pady=10)
title_label.pack(fill="x")

# Create a canvas with scrollbar for scrolling
canvas = tk.Canvas(main_frame, bg="#1c1c1c")
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

# Configure canvas to expand with the window
# main_frame.bind("<Configure>", lambda e: canvas.configure(width=e.width-20))

# Frame for user info
frame = tk.Frame(scrollable_frame, bg="#262626", padx=20, pady=20, relief="ridge", borderwidth=1)
frame.pack(fill="x",expand=True)


# profile picture with border
label_image = tk.Label(frame, bg="#1c1c1c", relief="solid", bd=2)
label_image.grid(row=0, column=0, rowspan=5, padx=30)

label_user_id = tk.Label(frame, text="Username: ", font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_user_id.grid(row=0, column=3, pady=5, padx=600)

label_name = tk.Label(frame, text="Name: ", font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_name.grid(row=1, column=3, pady=5)

label_email = tk.Label(frame, text="Email: ", font=("Arial", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_email.grid(row=2, column=3, pady=5)

label_age = tk.Label(frame, text="Age: ", font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_age.grid(row=3, column=3, pady=5)

label_phone_number = tk.Label(frame, text="Phone: ", font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_phone_number.grid(row=4, column=3, pady=5)

label_cooking_type = tk.Label(frame, text="Cook Type: ", font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_cooking_type.grid(row=5, column=3, pady=5)

label_experience = tk.Label(frame, text="Experience: ", font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_experience.grid(row=6, column=3, pady=5)

label_bio = tk.Label(frame,text="bio: ",font=("Helvetica", 16), bg="#262626", fg="#ffffff", anchor="center",width=30)
label_bio.grid(row=7, column=3, pady=5)

#frame for user posts
frame = tk.Frame(scrollable_frame, bg="#262626", padx=20, pady=20, relief="ridge", borderwidth=1)
frame.pack(fill="x")
posts_label = tk.Label(frame, text="User Posts:-", font=("Helvetica", 16, "bold"), bg="#262626", fg="#f46464", anchor="center",width=30)
posts_label.grid(row=0, column=0, pady=5)

# Create a card container
BG_COLOR = "#262626"
TEXT_COLOR = "#ffffff"
TITLE_FONT = ("Arial", 14, "bold")
DESC_FONT = ("Arial", 10)
ICON_FONT = ("Arial", 12)
USERNAME_FONT = ("Arial", 10, "italic")



# Enable mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

print(sys.argv[1])
display_profile(str(sys.argv[1]))
display_posts(main_id)

root.state("zoomed")
root.mainloop()