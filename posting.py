import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector


class CookbookAPP:
    def __init__(self,root):
        self.root = root
        self.root.title("Simple Food Entry Form")

        self.image_data = None
        self.create_widgets()

   # Validate numeric input(for duration)
    def validate_numeric_input(self, P):
        if P.isdigit() or P == "":
            return True
        else:
            return False

    # Validate rating input (1-5)
    def validate_rating_input(self, P):
        if P.isdigit() and (P == "" or 1 <= int(P) <= 5):
            return True
        else:
            return False

    def create_widgets(self):
    # Name
        self.name_label = tk.Label(self.root, text = "Name",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.name_label.grid(row=0,column=0,padx=10,pady=5,sticky="w")
        self.name_entry = tk.Entry(self.root, font=("Helvetica" , 14),width=30)
        self.name_entry.grid(row=0,column=1,padx=10,pady=5,sticky="ew")

    # Description
        self.description_label = tk.Label(self.root, text="Description:",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.description_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = tk.Text(self.root, height=6,font=("Helvetica" , 14))
        self.description_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
    #  Tags
        self.tags_label = tk.Label(self.root, text="Tags:",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.tags_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.tags_entry = tk.Entry(self.root,font=("Helvetica" , 14),width=30)
        self.tags_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
    #  Duration
        self.duration_label = tk.Label(self.root, text="Duration (minutes):",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.duration_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), '%P'),font=("Helvetica" , 14),width=30)
        self.duration_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
    #  Rating
        self.rating_label = tk.Label(self.root, text="Rating (1-5):",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.rating_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.rating_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_rating_input), '%P'),font=("Helvetica" , 14),width=30)
        self.rating_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
    #    Category
        self.category_label = tk.Label(self.root, text="Category:",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.category_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.category_options = ["Appetizer", "Main Course", "Dessert", "Beverage", "Snack"]
        self.category_dropdown = ttk.Combobox(self.root, values=self.category_options,font=("Helvetica", 14), width=27)
        self.category_dropdown.set("Select Category")
        self.category_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="ew")  

    # Ingredients
        self.ingredient_label = tk.Label(self.root, text="Ingredients:",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.ingredient_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.ingredient_entry = tk.Text(self.root, height=4,font=("Helvetica", 14))
        self.ingredient_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

     # Image
        self.image_label = tk.Label(self.root, text="No image selected",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10)
        self.image_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.image_button = tk.Button(self.root, text="Select Image", command=self.upload_image,font=("Helvetica", 14), bg="#00796b", fg="white")
        self.image_button.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    #  Submit Button
        self.submit_button = tk.Button(self.root, text="Submit",font=("Helvetica", 24, "bold"), bg="#00796b", fg="white", padx=10, pady=10, command=self.insert_data)
        self.submit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=20)
      

# open file dialog to upload an image
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;.jpeg;.gif")])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.image_data = file.read()
            
                # Load the original image
                original_image = Image.open(file_path)
                image = original_image.resize((400, 400))
                img_tk = ImageTk.PhotoImage(image)
            
                self.image_label.config(image=img_tk, text="")
                self.image_label.image = img_tk #keep a reference
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read image: {e}")


# Establish connection to the database
    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host ="localhost",
                user = "root",
                password ="password123",
                database ="cookbook"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error",f"failed to connect: {err}")
            return None

# Insert from data into the database

    def insert_data(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Name is requred")
            return

        description = self.description_entry.get("1.0", tk.END).strip()
        tags = self.tags_entry.get()
        duration = self.duration_entry.get()
        rating = self.rating_entry.get()
        category = self.category_dropdown.get()
        ingredient = self.ingredient_entry.get("1.0", tk.END).strip()
        
        if not self.image_data:
            messagebox.showwarning("Input Error", "Please select an image") 
            return
    
# connect to the database
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
                messagebox.showinfo("Success", "Data inserted successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("SQL Error", f"Failed to insert data: {err}")
            finally:
                conn.close()


# Create the main window
root = tk.Tk()
app = CookbookAPP(root)

root.state("zoomed")
# Start the main loop
root.mainloop()
