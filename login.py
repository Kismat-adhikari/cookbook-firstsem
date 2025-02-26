import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import mysql.connector
import os
import re
import bcrypt

image_data = None

def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='cookbook',
            user='root',
            password='password123'
        )
        if connection.is_connected():
            print("connected!")
            return connection
    except mysql.connector.Error as e:
        print("ERROR: \n", e)
        messagebox.showerror("Database Error", f"Connection failed: {e}")

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.webp")])
    if file_path:
        global image_data
        try:
            with open(file_path, 'rb') as file:
                image_data = file.read()
            
            # Load the original image
            original_image = Image.open(file_path)
            
            # Resize to a much larger size - 400x400 pixels
            image = original_image.resize((400, 400))
            
            img_tk = ImageTk.PhotoImage(image)
            
            # Update the label with the new image
            label_image.config(image=img_tk)
            label_image.image = img_tk  # Keep a reference to prevent garbage collection
            
            # Reset width and height to accommodate the image
            label_image.config(width=400, height=400)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read image: {e}")
            
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def store_data(fullname_entry, username_entry, email_entry, age_entry, phone_entry, experience, cook_type, password_entry, confirm_password_entry, error_label):
    # to verify data is not being repeated
    if not fullname_entry.get() or not username_entry.get() or not email_entry.get() or not password_entry.get():
        messagebox.showerror("Error", "Please fill in all required fields")
        return
    
    if fullname_entry.get().istitle() == False:
        error_label.config(text="Name must start with a capital letter!")
        return
    
    if is_valid_email(email_entry.get()) == None:
        error_label.config(text="Invalid email address!")
        return

    if password_entry.get() != confirm_password_entry.get():
        error_label.config(text="Passwords do not match!")  
        return

    error_label.config(text="")

    hashed_password = bcrypt.hashpw(password_entry.get().encode('utf-8'), bcrypt.gensalt())
    password_entry.delete(0, tk.END)
    confirm_password_entry.delete(0, tk.END)

    connection = connect()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO profile (name, username, email, age, phone_number, experience, cook_type, password, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (fullname_entry.get(), username_entry.get(), email_entry.get(), age_entry.get(), phone_entry.get(), experience.get(), cook_type.get(), hashed_password, image_data))
            connection.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            name = fullname_entry.get()
            root.destroy() 
            goto_profile(name)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to store data: {e}")
        finally:
            connection.close()

def goto_profile(name):
    connection = connect() 
    if connection:
        cursor= connection.cursor()
        try:
            cursor.execute("SELECT id FROM profile WHERE name = %s", (name,))
            id = cursor.fetchone()[0]
            os.system(f'python user_profile.py {id}')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open profile page: {e}")

def check_login(username_email_entry, password_entry):
    if not username_email_entry.get() or not password_entry.get():
        messagebox.showerror("Error", "Please enter username/email and password")
        return
        
    connection = connect()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name, password FROM profile WHERE username = %s OR email = %s", 
                        (username_email_entry.get(), username_email_entry.get()))
            user = cursor.fetchone()
            if user:
                name = user[0]
                password = user[1].encode()
                if bcrypt.checkpw(password_entry.get().encode(), password):
                    root.destroy()
                    goto_profile(name)
                else:
                    messagebox.showerror("Error", "Invalid Password")
            else:
                messagebox.showerror("Error", "User not found")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Login failed: {e}")
        finally:
            connection.close()

def switch_to_signup():
    global main_frame, label_image
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Create a canvas with scrollbar for scrolling
    canvas = tk.Canvas(main_frame, bg="#1c1c1c")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    
    # Configure the scrollable frame
    scrollable_frame = tk.Frame(canvas, bg="#1c1c1c")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Create a window inside the canvas to hold the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Configure canvas to expand with the window
    main_frame.bind("<Configure>", lambda e: canvas.configure(width=e.width-20))  # 20 px for scrollbar

    # Create a frame with padding and border for better visibility
    signup_frame = tk.Frame(scrollable_frame, bg="#1c1c1c", bd=1, relief="solid")
    signup_frame.pack(padx=40, pady=40, fill="both", expand=True)

    # Header with better spacing
    header_frame = tk.Frame(signup_frame, bg="#1c1c1c")
    header_frame.pack(fill="x", pady=20)
    
    tk.Label(header_frame, text="Create a New Account", font=("Arial", 24, "bold"), bg="#1c1c1c", fg="#f46464").pack()

    # Create a container for form fields
    form_frame = tk.Frame(signup_frame, bg="#1c1c1c")
    form_frame.pack(fill="both", expand=True, padx=30, pady=10)

    # Fields with better spacing and alignment
    fields_frame = tk.Frame(form_frame, bg="#1c1c1c")
    fields_frame.pack(fill="both", expand=True)

    # Left column - Personal info
    left_column = tk.Frame(fields_frame, bg="#1c1c1c")
    left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    fields_left = [("Full Name", None), ("Username", None), ("Email", None), ("Age", None)]
    entries_left = []
    
    for field, show in fields_left:
        field_frame = tk.Frame(left_column, bg="#1c1c1c")
        field_frame.pack(fill="x", pady=8)
        
        tk.Label(field_frame, text=field, font=("Arial", 12), bg="#1c1c1c", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        entry = tk.Entry(field_frame, font=("Arial", 12), width=25, bd=1, relief="solid", bg="#333333", fg="white", insertbackground="white")
        if show:
            entry.config(show=show)
        entry.pack(fill="x", ipady=4)
        entries_left.append(entry)
    
    fullname_entry, username_entry, email_entry, age_entry = entries_left

    # Right column - Account info
    right_column = tk.Frame(fields_frame, bg="#1c1c1c")
    right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    fields_right = [("Phone", None), ("Password", "*"), ("Confirm Password", "*")]
    entries_right = []
    
    for field, show in fields_right:
        field_frame = tk.Frame(right_column, bg="#1c1c1c")
        field_frame.pack(fill="x", pady=8)
        
        tk.Label(field_frame, text=field, font=("Arial", 12), bg="#1c1c1c", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        entry = tk.Entry(field_frame, font=("Arial", 12), width=25, bd=1, relief="solid", bg="#333333", fg="white", insertbackground="white")
        if show:
            entry.config(show=show)
        entry.pack(fill="x", ipady=4)
        entries_right.append(entry)
    error_label = tk.Label(signup_frame, text="", font=("Arial", 12), bg="#1c1c1c", fg="red")
    error_label.pack(fill="x", pady=(5, 10))
    
    phone_entry, password_entry, confirm_password_entry = entries_right

    # Experience dropdown
    exp_frame = tk.Frame(left_column, bg="#1c1c1c")
    exp_frame.pack(fill="x", pady=8)
    
    tk.Label(exp_frame, text="Experience", font=("Arial", 12), bg="#1c1c1c", fg="white").pack(anchor="w", pady=(0, 2))
    experience = ttk.Combobox(exp_frame, values=["Less then 1 year"] + ["More then 1 years"] + ["More then 3 years"] + ["More then 5 years"] + ["More then 8 years"] + ["More then 10 years"], state="readonly", font=("Arial", 11))
    experience.pack(fill="x", ipady=3)
    experience.current(0)

    # Cook type dropdown
    cook_frame = tk.Frame(right_column, bg="#1c1c1c")
    cook_frame.pack(fill="x", pady=8)
    
    tk.Label(cook_frame, text="Cook Type", font=("Arial", 12), bg="#1c1c1c", fg="white").pack(anchor="w", pady=(0, 2))
    cook_type = ttk.Combobox(cook_frame, values=["Vegetarian", "Non-Vegetarian", "Vegan", "Dessert Specialist"], state="readonly", font=("Arial", 11))
    cook_type.pack(fill="x", ipady=3)

    # Profile picture section - Improved layout for bigger image
    pic_frame = tk.Frame(signup_frame, bg="#1c1c1c")
    pic_frame.pack(fill="x", padx=30, pady=10)
    
    pic_header = tk.Label(pic_frame, text="Profile Picture", font=("Arial", 12, "bold"), bg="#1c1c1c", fg="white")
    pic_header.pack(anchor="w", pady=(10, 5))
    
    pic_content = tk.Frame(pic_frame, bg="#1c1c1c")
    pic_content.pack(fill="x")
    
    # Left side - button
    upload_section = tk.Frame(pic_content, bg="#1c1c1c")
    upload_section.pack(side="left", padx=(0, 20))
    
    upload_photo_button = tk.Button(upload_section, text="Upload Profile Picture", command=upload_image, 
                                    bg="#f46464", fg="white", font=("Arial", 12), padx=10, pady=5)
    upload_photo_button.pack(pady=10)
    
    # Right side - image preview (improved for actual pixel dimensions)
    preview_section = tk.Frame(pic_content, bg="#1c1c1c")
    preview_section.pack(side="right", padx=(20, 0))

    # Don't specify width/height in character units
    label_image = tk.Label(preview_section, bg="#333333", fg="white", text="Image Preview")
    label_image.pack(pady=10)

    # Buttons section with better spacing
    button_frame = tk.Frame(signup_frame, bg="#1c1c1c")
    button_frame.pack(fill="x", padx=30, pady=20)
    
    signup_button = tk.Button(button_frame, text="Sign Up", 
                              command=lambda: store_data(fullname_entry, username_entry, email_entry, age_entry, 
                                                         phone_entry, experience, cook_type, password_entry, confirm_password_entry, error_label),
                              bg="#f46464", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
    signup_button.pack(fill="x", pady=(0, 10))
    
    login_button = tk.Button(button_frame, text="Back to Login", command=switch_to_login, 
                             bg="#444444", fg="white", font=("Arial", 12), padx=10, pady=5)
    login_button.pack(fill="x")

    # Enable mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

def switch_to_login():
    global main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    main_frame.configure(bg="#1c1c1c")

    # Create a frame with padding and border for better visibility
    login_frame = tk.Frame(main_frame, bg="#1c1c1c", bd=1, relief="solid")
    login_frame.pack(padx=40, pady=40, fill="both", expand=True)

    # Header with better spacing
    header_frame = tk.Frame(login_frame, bg="#1c1c1c")
    header_frame.pack(fill="x", pady=25)
    
    tk.Label(header_frame, text="Login", font=("Arial", 24, "bold"), bg="#1c1c1c", fg="#f46464").pack()

    # Form fields with better spacing
    form_frame = tk.Frame(login_frame, bg="#1c1c1c")
    form_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    # Username/Email field
    username_frame = tk.Frame(form_frame, bg="#1c1c1c")
    username_frame.pack(fill="x", pady=12)
    
    tk.Label(username_frame, text="Username or Email", font=("Arial", 12), bg="#1c1c1c", fg="white").pack(anchor="w", pady=(0, 3))
    username_email_entry = tk.Entry(username_frame, font=("Arial", 12), width=30, bd=1, relief="solid", bg="#333333", fg="white", insertbackground="white")
    username_email_entry.pack(fill="x", ipady=5)

    # Password field
    password_frame = tk.Frame(form_frame, bg="#1c1c1c")
    password_frame.pack(fill="x", pady=12)
    
    tk.Label(password_frame, text="Password", font=("Arial", 12), bg="#1c1c1c", fg="white").pack(anchor="w", pady=(0, 3))
    password_entry = tk.Entry(password_frame, show="*", font=("Arial", 12), width=30, bd=1, relief="solid", bg="#333333", fg="white", insertbackground="white")
    password_entry.pack(fill="x", ipady=5)

    # Buttons with better spacing and colors
    button_frame = tk.Frame(login_frame, bg="#1c1c1c")
    button_frame.pack(fill="x", padx=40, pady=30)
    
    login_button = tk.Button(button_frame, text="Login", command=lambda: check_login(username_email_entry, password_entry), 
                             bg="#f46464", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
    login_button.pack(fill="x", pady=(0, 10))
    
    signup_button = tk.Button(button_frame, text="Sign Up", command=switch_to_signup, 
                              bg="#444444", fg="white", font=("Arial", 12), padx=10, pady=5)
    signup_button.pack(fill="x")

# Initialize application
root = tk.Tk()
root.title("Login and Signup")

# Significantly increased window size for the larger image
window_width = 950
window_height = 850
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
#zoom the windoiw to full screen
root.state("zoomed")# do not change this line

# Create main frame with better background
main_frame = tk.Frame(root, bg="#1c1c1c")
main_frame.pack(expand=True, fill="both")

# Start with login screen
switch_to_login()

root.mainloop()