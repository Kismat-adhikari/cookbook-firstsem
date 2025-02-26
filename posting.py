import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import mysql.connector
import os
import sys
from datetime import datetime

# Define colors for navbar
BG_DARK = "#1c1c1c"
BG_MEDIUM = "#262626"
ACCENT_COLOR = "#f46464"
TEXT_COLOR = "#ffffff"
LABEL_FONT = ("Segoe UI", 12)

# Navigation functions
def open_feed():
    root.destroy()
    # Assuming you have a feed.py file in the same directory
    os.system(f'python {os.path.join(os.path.dirname(__file__), "feed.py")} {sys.argv[1]}')

def open_posting():
    # Already on posting page, do nothing
    pass

def open_profile():
    root.destroy()
    # Assuming you have a user_profile.py file in the same directory
    os.system(f'python {os.path.join(os.path.dirname(__file__), "user_profile.py")} {sys.argv[1]}')

def logout():
    root.destroy()
    # Return to login page
    os.system(f'python {os.path.join(os.path.dirname(__file__), "logintest.py")}')

class ModernCookbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gourmet Recipe Manager")
        self.root.configure(bg=BG_DARK)
        
        # Navbar Frame
        self.navbar_frame = tk.Frame(self.root, bg=BG_MEDIUM, height=50)
        self.navbar_frame.pack(fill="x")
        self.navbar_frame.pack_propagate(False)  # Prevent frame from shrinking

        # Navbar Buttons
        self.feed_btn = tk.Button(self.navbar_frame, text="Feed", font=LABEL_FONT, bg=BG_MEDIUM, fg=TEXT_COLOR, bd=0, command=open_feed)
        self.feed_btn.pack(side="left", padx=20, pady=10)

        self.posting_btn = tk.Button(self.navbar_frame, text="Posting", font=LABEL_FONT, bg=ACCENT_COLOR, fg=TEXT_COLOR, bd=0)
        self.posting_btn.pack(side="left", padx=20, pady=10)

        self.profile_btn = tk.Button(self.navbar_frame, text="Profile", font=LABEL_FONT, bg=BG_MEDIUM, fg=TEXT_COLOR, bd=0, command=open_profile)
        self.profile_btn.pack(side="left", padx=20, pady=10)

        self.logout_btn = tk.Button(self.navbar_frame, text="Logout", font=LABEL_FONT, bg=BG_MEDIUM, fg=TEXT_COLOR, bd=0, command=logout)
        self.logout_btn.pack(side="right", padx=20, pady=10)
        
        # Set app icon if available
        try:
            self.root.iconbitmap("cookbook_icon.ico")
        except:
            pass
        
        # Variables
        self.image_data = None
        self.image_path = None
        self.preview_image = None
        
        # Create main scrollable canvas
        self.create_scrollable_canvas()
        
        # Configure styles
        self.setup_styles()
        
        # Create UI elements
        self.create_widgets()
        
    def create_scrollable_canvas(self):
        # Create canvas with scrollbar using pack instead of grid
        self.canvas_frame = tk.Frame(self.root, bg=BG_DARK)
        self.canvas_frame.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.main_canvas = tk.Canvas(self.canvas_frame, bg=BG_DARK, highlightthickness=0, 
                                     yscrollcommand=self.scrollbar.set)
        self.main_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.main_canvas.yview)

        # Create frame inside canvas for content
        self.scroll_frame = tk.Frame(self.main_canvas, bg=BG_DARK)
        self.main_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Configure scrollregion
        self.scroll_frame.bind(
            "<Configure>", 
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        # Update the inner frame's width to fill the canvas
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def on_mousewheel(self, event):
        # Scroll with mousewheel
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_styles(self):
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Combobox style
        self.style.configure(
            'TCombobox', 
            fieldbackground='#ff7676',
            background='#ff7676',
            selectbackground='#FF7676',
            selectforeground='white'
        )
        
        # Scrollbar style
        self.style.configure(
            'TScrollbar',
            background='#FF5252',
            troughcolor='#f0f0f0',
            borderwidth=0,
            arrowsize=14
        )
        
    def validate_numeric_input(self, P):
        if P.isdigit() or P == "":
            return True
        else:
            return False

    def validate_rating_input(self, P):
        if P == "":
            return True
        try:
            value = int(P)
            return 1 <= value <= 5
        except ValueError:
            return False
            
    def create_widgets(self):
        # Main container with padding
        self.main_frame = tk.Frame(self.scroll_frame, bg=BG_DARK, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App header
        self.title_frame = tk.Frame(self.main_frame, bg=BG_DARK)
        self.title_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = tk.Label(
            self.title_frame, 
            text="Gourmet Recipe Collection", 
            font=("Helvetica", 28, "bold"), 
            bg=BG_DARK, 
            fg=ACCENT_COLOR
        )
        self.title_label.pack(pady=10)
        
        # Two-column layout
        self.content_frame = tk.Frame(self.main_frame, bg=BG_DARK)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Basic info
        self.left_frame = tk.Frame(self.content_frame, bg=BG_DARK, padx=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right column - Description, ingredients and image
        self.right_frame = tk.Frame(self.content_frame, bg=BG_DARK, padx=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create form fields
        self.create_basic_info_fields()
        self.create_description_fields()
        self.create_image_section()
        self.create_action_buttons()
        
    def create_basic_info_fields(self):
        # Basic info section
        self.basic_info_frame = tk.LabelFrame(
            self.left_frame, 
            text="Recipe Information", 
            font=("Helvetica", 14, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR,
            padx=15,
            pady=15
        )
        self.basic_info_frame.pack(fill=tk.X, pady=10)
        
        # Name
        self.name_label = tk.Label(
            self.basic_info_frame, 
            text="Recipe Name", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.name_label.pack(anchor="w", pady=(0, 5))
        
        self.name_entry = tk.Entry(
            self.basic_info_frame, 
            font=("Helvetica", 12), 
            width=30, 
            bd=2, 
            relief=tk.SOLID
        )
        self.name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Category
        self.category_label = tk.Label(
            self.basic_info_frame, 
            text="Category", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.category_label.pack(anchor="w", pady=(0, 5))
        
        self.category_options = ["Appetizer", "Main Course", "Dessert", "Beverage", "Snack", "Breakfast", "Lunch", "Dinner", "Salad", "Soup"]
        self.category_dropdown = ttk.Combobox(
            self.basic_info_frame,  
            values=self.category_options,  
            font=("Helvetica", 12),
            state="readonly"  # Add this line to make it read-only

        )
        self.category_dropdown.set("Select Category")
        self.category_dropdown.pack(fill=tk.X, pady=(0, 15))
        
        # Duration
        self.duration_label = tk.Label(
            self.basic_info_frame, 
            text="Preparation Time (minutes)", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.duration_label.pack(anchor="w", pady=(0, 5))
        
        self.duration_entry = tk.Entry(
            self.basic_info_frame, 
            validate="key", 
            validatecommand=(self.root.register(self.validate_numeric_input), '%P'), 
            font=("Helvetica", 12), 
            bd=2, 
            relief=tk.SOLID
        )
        self.duration_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Rating
        self.rating_label = tk.Label(
            self.basic_info_frame, 
            text="Rating (1-5)", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.rating_label.pack(anchor="w", pady=(0, 5))
        
        self.rating_frame = tk.Frame(self.basic_info_frame, bg=BG_DARK)
        self.rating_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.rating_var = tk.IntVar()
        self.rating_var.set(0)
        
        # Star rating system
        for i in range(5):
            star_btn = tk.Radiobutton(
                self.rating_frame, 
                text="★", 
                variable=self.rating_var, 
                value=i+1, 
                indicatoron=0, 
                font=("Helvetica", 16), 
                bg=BG_DARK, 
                fg="#999999", 
                activebackground=BG_DARK, 
                activeforeground=ACCENT_COLOR,
                selectcolor=BG_DARK,
                bd=0, 
                highlightthickness=0,
                command=self.update_stars
            )
            star_btn.pack(side=tk.LEFT)
        
        # Tags
        self.tags_label = tk.Label(
            self.basic_info_frame, 
            text="Tags (comma separated)", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.tags_label.pack(anchor="w", pady=(0, 5))
        
        self.tags_entry = tk.Entry(
            self.basic_info_frame, 
            font=("Helvetica", 12), 
            bd=2, 
            relief=tk.SOLID
        )
        self.tags_entry.pack(fill=tk.X, pady=(0, 15))
        
    def create_description_fields(self):
        # Description section
        self.description_frame = tk.LabelFrame(
            self.right_frame, 
            text="Recipe Details", 
            font=("Helvetica", 14, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR,
            padx=15,
            pady=15
        )
        self.description_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Description
        self.description_label = tk.Label(
            self.description_frame, 
            text="Description", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.description_label.pack(anchor="w", pady=(0, 5))
        
        self.description_entry = scrolledtext.ScrolledText(
            self.description_frame, 
            height=5, 
            font=("Helvetica", 12), 
            bd=2, 
            relief=tk.SOLID, 
            wrap=tk.WORD
        )
        self.description_entry.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Ingredients
        self.ingredient_label = tk.Label(
            self.description_frame, 
            text="Ingredients (one per line)", 
            font=("Helvetica", 12, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR
        )
        self.ingredient_label.pack(anchor="w", pady=(0, 5))
        
        self.ingredient_entry = scrolledtext.ScrolledText(
            self.description_frame, 
            height=8, 
            font=("Helvetica", 12), 
            bd=2, 
            relief=tk.SOLID, 
            wrap=tk.WORD
        )
        self.ingredient_entry.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
    def create_image_section(self):
        # Image section - improved to show image better
        self.image_frame = tk.LabelFrame(
            self.left_frame, 
            text="Recipe Image", 
            font=("Helvetica", 14, "bold"), 
            bg=BG_DARK, 
            fg=TEXT_COLOR,
            padx=15,
            pady=15
        )
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Image container with fixed size for consistency
        self.image_container = tk.Frame(
            self.image_frame, 
            bg="#f0f0f0", 
            width=300, 
            height=300
        )
        self.image_container.pack(pady=10)
        self.image_container.pack_propagate(False)  # Prevent resizing
        
        # Image preview with better placement
        self.image_preview = tk.Label(
            self.image_container, 
            text="No image selected", 
            font=("Helvetica", 12), 
            bg="#f0f0f0"
        )
        self.image_preview.pack(fill=tk.BOTH, expand=True)
        
        # Button container
        self.image_button_frame = tk.Frame(self.image_frame, bg=BG_DARK)
        self.image_button_frame.pack(fill=tk.X, pady=5)
        
        # Image button
        self.image_button = tk.Button(
            self.image_button_frame, 
            text="Select Image", 
            command=self.upload_image, 
            font=("Helvetica", 12), 
            bg=ACCENT_COLOR, 
            fg="white", 
            activebackground="#FF7676", 
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.image_button.pack(pady=5)
        
    def create_action_buttons(self):
        # Buttons frame
        self.button_frame = tk.Frame(self.main_frame, bg=BG_DARK, pady=15)
        self.button_frame.pack(fill=tk.X)
        
        # Clear button
        self.clear_button = tk.Button(
            self.button_frame, 
            text="Clear Form", 
            command=self.clear_form, 
            font=("Helvetica", 14), 
            bg="#9E9E9E", 
            fg="white", 
            activebackground="#BDBDBD", 
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # Submit button
        self.submit_button = tk.Button(
            self.button_frame, 
            text="Save Recipe", 
            command=self.insert_data, 
            font=("Helvetica", 14, "bold"), 
            bg=ACCENT_COLOR, 
            fg="white", 
            activebackground="#FF7676", 
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.submit_button.pack(side=tk.RIGHT, padx=10)
        
        # Status bar
        self.status_bar = tk.Label(
            self.main_frame, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W, 
            font=("Helvetica", 10), 
            bg="#f0f0f0", 
            fg="#555555",
            padx=10
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
    def update_stars(self):
        rating = self.rating_var.get()
        for i, widget in enumerate(self.rating_frame.winfo_children()):
            if i < rating:
                widget.config(fg=ACCENT_COLOR)  # Filled star
            else:
                widget.config(fg="#999999")  # Empty star
    
    def clear_form(self):
        # Clear all form fields
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.tags_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.rating_var.set(0)
        self.update_stars()
        self.category_dropdown.set("Select Category")
        self.ingredient_entry.delete("1.0", tk.END)
        
        # Reset image preview
        self.image_data = None
        self.image_path = None
        self.image_preview.config(image="", text="No image selected")
        
        # Update status
        self.status_bar.config(text="Form cleared")
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")],
            title="Select Recipe Image"
        )
        
        if file_path:
            try:
                # Store the file path
                self.image_path = file_path
                
                # Read image data for database storage
                with open(file_path, 'rb') as file:
                    self.image_data = file.read()
                
                # Create a preview
                original_image = Image.open(file_path)
                
                # Get container size for proper resizing
                container_width = self.image_container.winfo_width() or 300
                container_height = self.image_container.winfo_height() or 300
                
                # Calculate aspect ratio and resize while maintaining aspect ratio
                width, height = original_image.size
                
                # Calculate the scaling factor to fit inside the container
                scale = min(container_width/width, container_height/height)
                new_size = (int(width * scale), int(height * scale))
                
                # Resize the image with high quality
                resized_image = original_image.resize(new_size, Image.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(resized_image)
                
                # Update preview
                self.image_preview.config(image=self.preview_image, text="")
                
                # Update status
                filename = os.path.basename(file_path)
                self.status_bar.config(text=f"Image selected: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.status_bar.config(text="Error loading image")
    
    # Database connection - maintaining compatibility with original code
    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password123",
                database="cookbook"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect: {err}")
            self.status_bar.config(text="Database connection failed")
            return None
    
    def validate_form(self):
        # Check recipe name
        if not self.name_entry.get().strip():
            messagebox.showwarning("Input Error", "A name is necessary")
            self.name_entry.focus_set()
            return False
        
        # Check category
        if self.category_dropdown.get() == "Select Category":
            messagebox.showwarning("Input Error", "A category is necessary")
            self.category_dropdown.focus_set()
            return False
        
        # Check preparation time
        if not self.duration_entry.get().strip():
            messagebox.showwarning("Input Error", "A preparation time is necessary")
            self.duration_entry.focus_set()
            return False
        
        # Check rating
        if self.rating_var.get() == 0:
            messagebox.showwarning("Input Error", "A rating is necessary")
            return False
        
        # Check tags
        if not self.tags_entry.get().strip():
            messagebox.showwarning("Input Error", "Tags are necessary")
            self.tags_entry.focus_set()
            return False
        
        # Check image
        if not self.image_data:
            messagebox.showwarning("Input Error", "An image is necessary")
            return False
        
        # Check description
        if not self.description_entry.get("1.0", tk.END).strip():
            messagebox.showwarning("Input Error", "A description is necessary")
            self.description_entry.focus_set()
            return False
        
        # Check ingredients
        if not self.ingredient_entry.get("1.0", tk.END).strip():
            messagebox.showwarning("Input Error", "Ingredients are necessary")
            self.ingredient_entry.focus_set()
            return False
        
        return True
    
    # Insert data function - updated with comprehensive validation
    def insert_data(self):
        # Validate all required fields before proceeding
        if not self.validate_form():
            return
            
        # Get values from form elements
        name = self.name_entry.get().strip()
        description = self.description_entry.get("1.0", tk.END).strip()
        tags = self.tags_entry.get().strip()
        duration = self.duration_entry.get().strip()
        rating = str(self.rating_var.get())
        category = self.category_dropdown.get()
        ingredient = self.ingredient_entry.get("1.0", tk.END).strip()
        
        # Connect to the database
        conn = self.connect_to_database()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("USE cookbook")
                cursor.execute(''' 
                    INSERT INTO posts (name, detail, tags, duration, rating, category, ingredient, image, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (name, description, tags, duration, rating, category, ingredient, self.image_data, 1))
                conn.commit()
                messagebox.showinfo("Success", "Recipe saved successfully")
                
                # Clear form after successful save
                self.clear_form()
                self.status_bar.config(text="Recipe saved successfully")
                
            except mysql.connector.Error as err:
                messagebox.showerror("SQL Error", f"Failed to save recipe: {err}")
                self.status_bar.config(text="Error saving recipe")
            finally:
                conn.close()

# Application entry point
if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")  # Maximize the window
    app = ModernCookbookApp(root)
    root.mainloop()