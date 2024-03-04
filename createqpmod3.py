import tkinter as tk
from tkinter import messagebox
import mysql.connector
import createqpmod4  # Import the module for adding questions from Module 2
from closeall import WindowManager


def create_qp_mod3(parent,window_manager):
    root = tk.Tk()
    root.title("Create Question Paper")
    root.attributes('-fullscreen', True)  # Open in full screen
    selected_questions = []

    label = tk.Label(root, text="ADD QUESTIONS TO THE QUESTION PAPER FROM MODULE-3", font=('Arial', 18))
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

    # Define function to fetch module 3 questions from the database
    def fetch_module3_questions():
        # Connect to the database
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=""
        )
        cur = con.cursor()

        # Fetch questions from module 3
        cur.execute("SELECT module_3_questions FROM module3")
        module3_questions = [question[0] for question in cur.fetchall()]

        # Close the cursor and database connection
        cur.close()
        con.close()

        return module3_questions

    # Fetch questions from module 1 in the database
    module3_questions = fetch_module3_questions()

    # Create checkboxes for each question from Module 1
    for index, question in enumerate(module3_questions, start=1):
        checkbox = tk.Checkbutton(frame, text=question, command=lambda q=question: toggle_question(q))
        checkbox.pack(anchor=tk.W)

    # Define function to add selected questions to qpmod3
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
        query = "INSERT INTO qpmod3 (questions) VALUES (%s)"

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
        messagebox.showinfo("Success", "Selected questions have been added to qpmod3.")

    # Add button to add selected questions to qpmod1
    add_button = tk.Button(root, text="Add", command=add_questions)
    add_button.pack(pady=10)

    # Define function to open window for adding questions from Module 2
    def add_module4_questions():
        createqpmod4.create_qp_mod4(root,window_manager)

    # Add button to add questions from Module 2
    add_module4_button = tk.Button(root, text="Add Questions To Module 4", command=add_module4_questions)
    add_module4_button.pack(pady=10)

    window_manager.add_window(root)
    root.mainloop()
