# createqpmod5.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from closeall import WindowManager

def create_qp_mod5(parent,window_manager):
    root = tk.Tk()
    root.title("Create Question Paper")
    root.attributes('-fullscreen', True)  # Open in full screen
    selected_questions = []

    label = tk.Label(root, text="ADD QUESTIONS TO THE QUESTION PAPER FROM MODULE-4", font=('Arial', 18))
    label.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack()

    # Define function to toggle question selection
    def toggle_question(question):
        nonlocal selected_questions
        if question in selected_questions:
            selected_questions.remove(question)
        else:
            selected_questions.append(question)

    # Define function to fetch module 5 questions from the database
    def fetch_module5_questions():
        # Connect to the database
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=""
        )
        cur = con.cursor()

        # Fetch questions from module 5
        cur.execute("SELECT module_5_questions FROM module5")
        module5_questions = [question[0] for question in cur.fetchall()]

        # Close the cursor and database connection
        cur.close()
        con.close()

        return module5_questions

    # Fetch questions from module 5 in the database
    module5_questions = fetch_module5_questions()

    # Create checkboxes for each question from Module 5
    for index, question in enumerate(module5_questions, start=1):
        checkbox = tk.Checkbutton(frame, text=question, command=lambda q=question: toggle_question(q))
        checkbox.pack(anchor=tk.W)

    # Define function to add selected questions to qpmod5
    def add_questions():
        nonlocal selected_questions
        if len(selected_questions) != 8:
            messagebox.showwarning("Warning", "Please select 8 questions.")
            return

        # Connect to the database
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=""
        )

        # Prepare the INSERT statement
        query = "INSERT INTO qpmod5 (questions) VALUES (%s)"

        # Execute the INSERT statement for each selected question
        cur = con.cursor()
        for question in selected_questions:
            cur.execute(query, (question,))
        
        # Commit the changes to the database
        con.commit()

        # Close the cursor and database connection
        cur.close()
        con.close()

        # Show a success message
        messagebox.showinfo("Success", "Selected questions have been added to qpmod5.")

    # Add button to add selected questions to qpmod5
    add_button = tk.Button(root, text="Add", command=add_questions)
    add_button.pack(pady=10)

    # Define function to go back to the home screen
    def gohome():
        print("Entered gohome")
        # Close all open windows
        window_manager.close_all_windows()
        
    # Add button to go back to the home screen
    home_button = tk.Button(root, text="EXIT", command=gohome)
    home_button.pack(pady=10)
    window_manager.add_window(root)
    root.mainloop()
