import tkinter as tk
from tkinter import messagebox
import create
import add_to_existing
import viewqb
import createqp
import viewqp
from closeall import WindowManager
# Create WindowManager instance
window_manager = WindowManager()



class Main:
    def __init__(self):
        self.gui1 = MyGui1()

class MyGui1:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Question Bank Management")
        self.root.configure(bg="#f0f0f0")
        self.root.attributes('-fullscreen', True)  # Open in full screen
        
        center_frame = tk.Frame(self.root, bg="#f0f0f0")
        center_frame.pack(expand=True)
        
        self.label = tk.Label(center_frame, text="Welcome to EchoQuest: Voice-Powered Question Paper Generation", font=('Arial',18), bg="#f0f0f0")
        self.label.pack(pady=20)
        
        self.button = tk.Button(center_frame, text="Start",  font=('Arial',18), command=self.start, bg="#4CAF50", fg="white")
        self.button.pack(pady=10)
        
    def start(self):
        self.root.withdraw()  # Hide the current window
        MyGui2(self.root)  # Pass the reference of the root window to MyGui2

class MyGui2:
    def __init__(self, root):
        self.root = root
        self.top = tk.Toplevel(root)  # Use the root window reference
        self.top.title("Question Paper Management")
        self.top.attributes('-fullscreen', True)  # Make the window fullscreen
        
        left_frame = tk.Frame(self.top)
        left_frame.pack(side=tk.LEFT, padx=10)
        
        self.question_bank_label = tk.Label(left_frame, text="Question Bank", font=('Arial',18))
        self.question_bank_label.pack(pady=10)
        
        self.create_new_button = tk.Button(left_frame, text="Create New", font=('Arial',14), command=self.create_new_clicked)
        self.create_new_button.pack(pady=5)
        
        self.add_to_existing_button = tk.Button(left_frame, text="Add to Existing", font=('Arial',14), command=self.add_clicked)
        self.add_to_existing_button.pack(pady=5)
        
        self.view_button = tk.Button(left_frame, text="View", font=('Arial',14),command=self.view_question_bank)
        self.view_button.pack(pady=5)
        
        right_frame = tk.Frame(self.top)
        right_frame.pack(side=tk.RIGHT, padx=10)
        
        self.question_paper_label = tk.Label(right_frame, text="Question Paper", font=('Arial',18))
        self.question_paper_label.pack(pady=10)
        
        self.create_button = tk.Button(right_frame, text="Create QP", font=('Arial',14), command=self.addtoqp)
        self.create_button.pack(pady=5)
        
        self.view_paper_button = tk.Button(right_frame, text="View", font=('Arial',14), command=self.displayqp)  
        self.view_paper_button.pack(pady=5)
        
        quit_button = tk.Button(self.top, text="Quit", font=('Arial',14), command=self.quit)
        quit_button.pack(side=tk.BOTTOM, pady=10)
        
    def create_new_clicked(self):
        self.top.withdraw()  # Hide MyGui2
        create.create_new_questionbank(self.top)  # Pass the top-level window reference
        
    def add_clicked(self):
        self.top.withdraw()  # Hide MyGui2
        add_to_existing.add_to_existing_questionbank(self.top)
        
    def view_question_bank(self):
        self.top.withdraw()  # Hide MyGui2
        viewqb.display_questions(self.top)  # Display viewqb.py in a new window
    
    def addtoqp(self):
        self.top.withdraw()
        createqp.create_qp(self.top,window_manager)
        
    def displayqp(self):
        self.top.withdraw()
        viewqp.display_questions_qp(self.top)
        
        
    def quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.top.destroy()
            self.root.destroy()
            



# Create and add instances of MyGui1 and MyGui2 to WindowManager
main = Main()
window_manager.add_window(main.gui1.root)

# Start the main loop
main.gui1.root.mainloop()