import tkinter as tk

def show_signup():
    login_frame.pack_forget()
    signup_frame.pack(pady=20)

def show_login():
    signup_frame.pack_forget()
    login_frame.pack(pady=20)

def signup():
    show_login()

def login():
    pass

root = tk.Tk()
root.title("Login & Signup")
root.geometry("300x300")

# Signup Section
signup_frame = tk.Frame(root, padx=20, pady=20)
tk.Label(signup_frame, text="Signup", font=("Arial", 14, "bold")).pack(pady=5)
entry_signup_user = tk.Entry(signup_frame, width=25)
entry_signup_user.pack(pady=5)
entry_signup_pass = tk.Entry(signup_frame, show="*", width=25)
entry_signup_pass.pack(pady=5)
tk.Button(signup_frame, text="Signup", command=signup, bg="#4CAF50", fg="white").pack(pady=10)
signup_link = tk.Label(signup_frame, text="Go to Login", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
signup_link.pack()
signup_link.bind("<Button-1>", lambda e: show_login())

# Login Section
login_frame = tk.Frame(root, padx=20, pady=20)
tk.Label(login_frame, text="Login", font=("Arial", 14, "bold")).pack(pady=5)
entry_login_user = tk.Entry(login_frame, width=25)
entry_login_user.pack(pady=5)
entry_login_pass = tk.Entry(login_frame, show="*", width=25)
entry_login_pass.pack(pady=5)
tk.Button(login_frame, text="Login", command=login, bg="#008CBA", fg="white").pack(pady=10)
login_link = tk.Label(login_frame, text="Go to Signup", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
login_link.pack()
login_link.bind("<Button-1>", lambda e: show_signup())

login_frame.pack(pady=20)
root.mainloop()
