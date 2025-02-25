import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Taste Tracker | Food Social Media")
root.configure(bg="#f0f2f5")  # Facebook-like background
root.state("zoomed")  # Make window full screen

# Modern color scheme
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1c1e21"
ACCENT_COLOR = "#e41e3f"  # Food-themed red
SECONDARY_COLOR = "#65676b"

# Font configuration
TITLE_FONT = ("Segoe UI", 22, "bold")
SUBTITLE_FONT = ("Segoe UI", 14)
BODY_FONT = ("Segoe UI", 11)
ICON_FONT = ("Segoe UI", 12)

# Function to create a post
def create_post(parent, title, author, description):
    # Create a card with better shadow effect
    post_container = tk.Frame(parent, bg="#f0f2f5", padx=10, pady=10)
    post_container.pack(fill="x")
    
    main_frame = tk.Frame(post_container, bg=BG_COLOR, padx=0, pady=0)
    main_frame.pack(fill="x")
    
    # Add shadow effect with multiple frames for depth
    for i in range(3):
        shadow = tk.Frame(post_container, bg=f"#{225-i*10:02x}{225-i*10:02x}{225-i*10:02x}")
        shadow.place(in_=main_frame, relx=1+0.002*i, rely=1+0.002*i, 
                    anchor="se", relwidth=1, relheight=1)
    main_frame.lift()
    
    # Header with profile info
    header_frame = tk.Frame(main_frame, bg=BG_COLOR, pady=8, padx=10)
    header_frame.pack(fill="x")
    
    profile_frame = tk.Frame(header_frame, bg=BG_COLOR)
    profile_frame.pack(side="left", anchor="w")
    
    username_label = tk.Label(profile_frame, text=f"Chef {author}", font=SUBTITLE_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    username_label.pack(anchor="w")
    time_label = tk.Label(profile_frame, text="Posted 2 hours ago", font=("Segoe UI", 9), fg=SECONDARY_COLOR, bg=BG_COLOR)
    time_label.pack(anchor="w")
    
    # Image with better aspect ratio and centering
    image_frame = tk.Frame(main_frame, bg=BG_COLOR)
    image_frame.pack(fill="x")
    
    try:
        # Try to load the actual image
        image = Image.open("testimage.jpeg")
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
    image_container = tk.Frame(image_frame, bg=BG_COLOR, width=window_width, height=target_height)
    image_container.pack()
    image_container.pack_propagate(False)  # Don't shrink to image size
    
    image_label = tk.Label(image_container, image=photo, bg=BG_COLOR)
    image_label.image = photo  # Keep reference to prevent garbage collection
    image_label.place(relx=0.5, rely=0.5, anchor="center")  # Center image
    
    # Content section with improved layout
    content_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10, pady=12)
    content_frame.pack(fill="x")
    
    food_name_label = tk.Label(content_frame, text=title, font=TITLE_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    food_name_label.pack(anchor="w")
    
    desc_label = tk.Label(content_frame, text=description, wraplength=470, font=BODY_FONT, fg=TEXT_COLOR, bg=BG_COLOR, justify="left")
    desc_label.pack(anchor="w", pady=(8, 12))
    
    # Details section with better icons and organization
    details_frame = tk.Frame(content_frame, bg=BG_COLOR)
    details_frame.pack(fill="x", pady=5)
    
    # Left column
    left_details = tk.Frame(details_frame, bg=BG_COLOR)
    left_details.pack(side="left", fill="y", anchor="w")
    
    category_label = tk.Label(left_details, text="🍽️ Italian Cuisine", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    category_label.pack(anchor="w", pady=3)
    
    prep_label = tk.Label(left_details, text="⏱️ Prep: 15 min | Cook: 25 min", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    prep_label.pack(anchor="w", pady=3)
    
    # Right column
    right_details = tk.Frame(details_frame, bg=BG_COLOR)
    right_details.pack(side="right", fill="y", anchor="e")
    
    difficulty_label = tk.Label(right_details, text="👨‍🍳 Difficulty: Easy", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    difficulty_label.pack(anchor="e", pady=3)
    
    servings_label = tk.Label(right_details, text="🍴 Serves: 4 people", font=BODY_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    servings_label.pack(anchor="e", pady=3)
    
    # Tags with better styling
    tags_frame = tk.Frame(content_frame, bg=BG_COLOR)
    tags_frame.pack(fill="x", pady=(10, 0))
    
    # Create styled tag buttons
    tags = ["Italian", "Pasta", "Dinner", "Vegetarian"]
    for tag in tags:
        tag_btn = tk.Label(tags_frame, text=f"#{tag}", font=("Segoe UI", 10), 
                          fg=ACCENT_COLOR, bg=f"#ffebee", padx=8, pady=2)
        tag_btn.pack(side="left", padx=(0, 8))
    
    # Engagement section with counts
    ttk.Separator(main_frame, orient='horizontal').pack(fill='x', padx=10, pady=15)
    stats_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10)
    stats_frame.pack(fill="x")
    
    likes_label = tk.Label(stats_frame, text="❤ 142 likes", font=BODY_FONT, fg=SECONDARY_COLOR, bg=BG_COLOR)
    likes_label.pack(side="left", padx=(0, 15))
    
    comments_label = tk.Label(stats_frame, text="💬 24 comments", font=BODY_FONT, fg=SECONDARY_COLOR, bg=BG_COLOR)
    comments_label.pack(side="left")
    
    ttk.Separator(main_frame, orient='horizontal').pack(fill='x', padx=10, pady=15)
    
    # Interaction buttons with better styling
    buttons_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10, pady=10)
    buttons_frame.pack(fill="x")
    
    # Like button functionality with closure to maintain state
    def create_toggle_like(like_button, likes_count):
        def toggle_like():
            if like_button["text"] == "♡ Like":
                like_button["text"] = "❤ Liked"
                like_button["fg"] = ACCENT_COLOR
                likes_count["text"] = "❤ 143 likes"
            else:
                like_button["text"] = "♡ Like"
                like_button["fg"] = TEXT_COLOR
                likes_count["text"] = "❤ 142 likes"
        return toggle_like
    
    # Better styled buttons
    like_btn = tk.Button(buttons_frame, text="♡ Like", font=BODY_FONT, fg=TEXT_COLOR, 
                        bg=BG_COLOR, bd=0, padx=10, pady=5,
                        activebackground="#f5f5f5")
    like_btn["command"] = create_toggle_like(like_btn, likes_label)
    like_btn.pack(side="left", padx=(0, 15))
    
    comment_btn = tk.Button(buttons_frame, text="💬 Comment", font=BODY_FONT, fg=TEXT_COLOR, 
                          bg=BG_COLOR, bd=0, padx=10, pady=5,
                          activebackground="#f5f5f5")
    comment_btn.pack(side="left", padx=(0, 15))
    
    save_btn = tk.Button(buttons_frame, text="🔖 Save", font=BODY_FONT, fg=TEXT_COLOR, 
                        bg=BG_COLOR, bd=0, padx=10, pady=5,
                        activebackground="#f5f5f5")
    save_btn.pack(side="left")
    
    return main_frame

# Create a canvas and scrollbar for the posts
canvas = tk.Canvas(root, bg=BG_COLOR)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

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

# Create posts inside the scrollable frame
for i in range(4):
    if i == 0:
        post = create_post(scrollable_frame, f'Post {i+1}', 'Author', 'Testing ho but desciption chai yo hunxaa')
    elif i == 1:
        post = create_post(scrollable_frame, f'Post {i+1}', 'Author', 'Another post ')
    elif i == 2:
        post = create_post(scrollable_frame, f'Post {i+1}', 'Author', 'This is the third post ')
    else:
        post = create_post(scrollable_frame, f'Post {i+1}', 'Author', 'This is the fourth post.')
    
    post.pack(fill='x', pady=10)

# Run the Tkinter main loop
root.mainloop()