import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import mysql.connector
import os

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
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
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
            
def store_data(fullname_entry, username_entry, email_entry, age_entry, phone_entry, experience, cook_type, password_entry):
    # Basic validation
    if not fullname_entry.get() or not username_entry.get() or not email_entry.get() or not password_entry.get():
        messagebox.showerror("Error", "Please fill in all required fields")
        return
        
    connection = connect()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO profile (name, username, email, age, phone_number, experience, cook_type, password, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (fullname_entry.get(), username_entry.get(), email_entry.get(), age_entry.get(), phone_entry.get(), experience.get(), cook_type.get(), password_entry.get(), image_data))
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
    try:
        os.system(f'python user_profile.py {name}')
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
                name, password = user
                if password == password_entry.get():
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
    canvas = tk.Canvas(main_frame, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    
    # Configure the scrollable frame
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
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
    signup_frame = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
    signup_frame.pack(padx=40, pady=40, fill="both", expand=True)

    # Header with better spacing
    header_frame = tk.Frame(signup_frame, bg="white")
    header_frame.pack(fill="x", pady=20)
    
    tk.Label(header_frame, text="Create a New Account", font=("Arial", 24, "bold"), bg="white", fg="#4CAF50").pack()

    # Create a container for form fields
    form_frame = tk.Frame(signup_frame, bg="white")
    form_frame.pack(fill="both", expand=True, padx=30, pady=10)

    # Fields with better spacing and alignment
    fields_frame = tk.Frame(form_frame, bg="white")
    fields_frame.pack(fill="both", expand=True)

    # Form Fields
    fields = ["Full Name", "Username", "Email", "Age", "Phone", "Password", "Confirm Password"]
    entries = []
    for i, field in enumerate(fields):
        tk.Label(scrollable_frame, text=field, font=("Arial", 14), bg="#f7f7f7").grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(scrollable_frame, font=("Arial", 14), width=30)
        entry.grid(row=i + 1, column=1, padx=10, pady=5)
        entries.append(entry)

    fullname_entry, username_entry, email_entry, age_entry, phone_entry, password_entry, confirm_password_entry = entries

    # Experience dropdown
    exp_frame = tk.Frame(left_column, bg="white")
    exp_frame.pack(fill="x", pady=8)
    
    tk.Label(exp_frame, text="Experience (years)", font=("Arial", 12), bg="white").pack(anchor="w", pady=(0, 2))
    experience = ttk.Combobox(exp_frame, values=["<1 year"] + [str(i) for i in range(1, 51)], state="readonly", font=("Arial", 11))
    experience.pack(fill="x", ipady=3)
    experience.current(0)

    # Cook type dropdown
    cook_frame = tk.Frame(right_column, bg="white")
    cook_frame.pack(fill="x", pady=8)
    
    tk.Label(cook_frame, text="Cook Type", font=("Arial", 12), bg="white").pack(anchor="w", pady=(0, 2))
    cook_type = ttk.Combobox(cook_frame, values=["Vegetarian", "Non-Vegetarian", "Vegan", "Dessert Specialist"], state="readonly", font=("Arial", 11))
    cook_type.pack(fill="x", ipady=3)

    # Profile picture section - Improved layout for bigger image
    pic_frame = tk.Frame(signup_frame, bg="white")
    pic_frame.pack(fill="x", padx=30, pady=10)
    
    pic_header = tk.Label(pic_frame, text="Profile Picture", font=("Arial", 12, "bold"), bg="white")
    pic_header.pack(anchor="w", pady=(10, 5))
    
    pic_content = tk.Frame(pic_frame, bg="white")
    pic_content.pack(fill="x")
    
    # Left side - button
    upload_section = tk.Frame(pic_content, bg="white")
    upload_section.pack(side="left", padx=(0, 20))
    
    upload_photo_button = tk.Button(upload_section, text="Upload Profile Picture", command=upload_image, 
                                    bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
    upload_photo_button.pack(pady=10)
    
    # Right side - image preview (improved for actual pixel dimensions)
    preview_section = tk.Frame(pic_content, bg="white")
    preview_section.pack(side="right", padx=(20, 0))

    # Don't specify width/height in character units
    label_image = tk.Label(preview_section, bg="#f0f0f0", text="Image Preview")
    label_image.pack(pady=10)

    # Buttons section with better spacing
    button_frame = tk.Frame(signup_frame, bg="white")
    button_frame.pack(fill="x", padx=30, pady=20)
    
    signup_button = tk.Button(button_frame, text="Sign Up", 
                              command=lambda: store_data(fullname_entry, username_entry, email_entry, age_entry, 
                                                         phone_entry, experience, cook_type, password_entry),
                              bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
    signup_button.pack(fill="x", pady=(0, 10))
    
    login_button = tk.Button(button_frame, text="Back to Login", command=switch_to_login, 
                             bg="#e0e0e0", fg="#333", font=("Arial", 12), padx=10, pady=5)
    login_button.pack(fill="x")

    # Enable mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

def switch_to_login():
    global main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    main_frame.configure(bg="#f0f0f0")

    # Create a frame with padding and border for better visibility
    login_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
    login_frame.pack(padx=40, pady=40, fill="both", expand=True)

    # Header with better spacing
    header_frame = tk.Frame(login_frame, bg="white")
    header_frame.pack(fill="x", pady=25)
    
    tk.Label(header_frame, text="Login", font=("Arial", 24, "bold"), bg="white", fg="#4CAF50").pack()

    # Form fields with better spacing
    form_frame = tk.Frame(login_frame, bg="white")
    form_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    # Username/Email field
    username_frame = tk.Frame(form_frame, bg="white")
    username_frame.pack(fill="x", pady=12)
    
    tk.Label(username_frame, text="Username or Email", font=("Arial", 12), bg="white").pack(anchor="w", pady=(0, 3))
    username_email_entry = tk.Entry(username_frame, font=("Arial", 12), width=30, bd=1, relief="solid")
    username_email_entry.pack(fill="x", ipady=5)

    # Password field
    password_frame = tk.Frame(form_frame, bg="white")
    password_frame.pack(fill="x", pady=12)
    
    tk.Label(password_frame, text="Password", font=("Arial", 12), bg="white").pack(anchor="w", pady=(0, 3))
    password_entry = tk.Entry(password_frame, show="*", font=("Arial", 12), width=30, bd=1, relief="solid")
    password_entry.pack(fill="x", ipady=5)

    # Buttons with better spacing and colors
    button_frame = tk.Frame(login_frame, bg="white")
    button_frame.pack(fill="x", padx=40, pady=30)
    
    login_button = tk.Button(button_frame, text="Login", command=lambda: check_login(username_email_entry, password_entry), 
                             bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8)
    login_button.pack(fill="x", pady=(0, 10))
    
    signup_button = tk.Button(button_frame, text="Sign Up", command=switch_to_signup, 
                              bg="#e0e0e0", fg="#333", font=("Arial", 12), padx=10, pady=5)
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
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create main frame with better background
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(expand=True, fill="both")

# Start with login screen
switch_to_login()

root.mainloop()