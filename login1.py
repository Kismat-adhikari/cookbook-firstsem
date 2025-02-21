from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk   
from tkinter import messagebox


class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")

 #-----------------------bg image--------------------
        try:
            img=Image.open(r"C:\Users\User\Desktop\DEEP_RED.jpg")
            img=img.resize((1600,900))

            self.bg=ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Error",f"Failed to load image:{e}")
            return

        bg_lbl= Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)


# ----------------left image---------------

        self.bg1=ImageTk.PhotoImage(file=r"C:\Users\User\Desktop\360_F_292203735_CSsyqyS6A4Z9Czd4Msf7qZEhoxjpzZl1.jpg")
        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=50,y=100,width=470,height=550)


# -----------------main frame--------------------

        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        # register_lbl=Label(frame,text = "REGISTER HERE",font=("timews new roman",20,"bold"),foreground="darkgreen",background="white")
        # register_lbl.place(x=20,y=20)

# ========================labels and entrys(firstname)  and (username)=========================
# row1
        fname=Label(frame,text="Full Name",font=("timews new roman",15,"bold"),foreground="Black",background="white")
        fname.place(x=50,y=100)

        fname_entry=ttk.Entry(frame,font=("timews new roman",20,"bold"))
        fname_entry.place(x=50,y=130,width=250)

        fname1=Label(frame,text="Username",font=("times new roman",15,"bold"),foreground="black",background="white")
        fname1.place(x=370,y=100)

        self.txt_fname1=ttk.Entry(frame,font=("times new roman",15,"bold"),foreground="black",background="white")
        self.txt_fname1.place(x=370,y=130,width=250)

        

# ============row2(Age and Experience) =============

        Experience=Label(frame,text="Experience(in years)",font=(" times new roman",15,"bold"),background="white",foreground="black")
        Experience.place(x=50,y=170)


        self.txt_Experience=ttk.Entry(frame,font=("times new roman",15))
        self.txt_Experience.place(x=50,y=200,width=250)

        age=Label(frame,text="Age",font=("times new roman",15,"bold"),background="white",foreground='black')
        age.place(x=370,y=170)

        self.txt_age=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txt_age.place(x=370,y=200,width=250)

# ============row3 (cooking type)=============
        cooking=Label(frame,text="Cooking_Type",font=("times new roman",15,"bold"),background="white",foreground="black")
        cooking.place(x=50,y=240)

        self.combo_cooking=ttk.Combobox(frame,font=("times new roman",15,"bold"),state = "readonly ")
        self.combo_cooking["values"]=("Select","Italian","Chinese","Mexican","Indian","Mediterranean")
        self.combo_cooking.place(x=50,y=270,width=250)
        self.combo_cooking.current(0)
        
        contact_a=Label(frame,text="Contact",font=("times new roman",15,"bold"),background="white",foreground="black")
        contact_a.place(x=370,y=240)

        self.txt_contact=ttk.Entry(frame,font=("times new roman",15))
        self.txt_contact.place(x=370,y=270,width=250)

        

if __name__== "__main__":
    root=Tk()
    app=Register(root)  
    root.mainloop()

