import tkinter as tk
from tkinter import messagebox
class MyGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        
        
        self.label = tk.Label(master=self.root, text="Your message", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)
        
        self.texbox = tk.Text(master=self.root, height=5, font = ("Arial", 16))
        self.texbox.pack(padx=10, pady=10)
        self.texbox.bind("<KeyPress>", self.show_key_message)
        
        
        self.check_state = tk.IntVar()
        
        self.check = tk.Checkbutton(self.root, text="Show Messagebox", font=("Arial", 18), variable=self.check_state)
        
        self.check.pack(padx=10, pady=10)
        
        self.button = tk.Button(self.root, text="Show Message", font = ("Arial", 18), command=self.show_massage)
        self.button.pack(padx=10, pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def show_massage(self):
        if self.check_state.get() == 0:
            print(self.texbox.get('1.0', tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.texbox.get("1.0", tk.END))
        
    def show_key_message(self, even: tk.Event):
        if even.keysym == "Return" and even.state == 20:
            self.show_massage()
            
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you want to quit?" ):
            self.root.destroy()         
    
if __name__ == "__main__":
    gui = MyGUI()