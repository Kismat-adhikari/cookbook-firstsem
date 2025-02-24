import tkinter as tk
from tkinter import ttk

class NavigationBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # initial style for buttons
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Helvetica', 10))

        # Simplified layout just for packing the buttons
        buttons = ['Home', 'Post', 'Profile']
        commands = [self.home_action, self.about_action, self.contact_action, self.settings_action]
        
        for btn_text, command in zip(buttons, commands):
            ttk.Button(self, text=btn_text, command=command).pack(side=tk.LEFT, padx=5)

    def home_action(self):
        print("Home clicked")

    def about_action(self):
        print("About clicked")

    def contact_action(self):
        print("Contact clicked")

    def settings_action(self):
        print("Settings clicked")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple Navigation Bar")
    root.geometry("600x400")

    navbar = NavigationBar(root)
    navbar.pack(fill=tk.X)

    # Fullscrean
    root.state("zoomed")

    root.mainloop()
