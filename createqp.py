import tkinter as tk
from tkinter import messagebox
import mysql.connector
import createqpmod2  # Import the module for adding questions from Module 2
from closeall import WindowManager


def create_qp(parent,window_manager):
    root = tk.Tk()
    root.title("Create Question Paper")
    root.attributes('-fullscreen', True)  # Open in full screen
    selected_questions = []

    label = tk.Label(root, text="ADD QUESTIONS TO THE QUESTION PAPER FROM MODULE-1", font=('Arial', 18))
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

    # Define function to fetch module 1 questions from the database
    def fetch_module1_questions():
        # Connect to the database
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=""
        )
        cur = con.cursor()
        def new():
            cur.execute("DROP TABLE IF EXISTS qpmod1, qpmod2, qpmod3, qpmod4, qpmod5")
            cur.execute("CREATE TABLE qpmod1(snno int PRIMARY KEY AUTO_INCREMENT, questions text)")
            cur.execute("CREATE TABLE qpmod2(snno int PRIMARY KEY AUTO_INCREMENT, questions text)")
            cur.execute("CREATE TABLE qpmod3(snno int PRIMARY KEY AUTO_INCREMENT, questions text)")
            cur.execute("CREATE TABLE qpmod4(snno int PRIMARY KEY AUTO_INCREMENT, questions text)")
            cur.execute("CREATE TABLE qpmod5(snno int PRIMARY KEY AUTO_INCREMENT, questions text)")
            con.commit()

        new()

        # Fetch questions from module 1
        cur.execute("SELECT module_1_questions FROM module1")
        module1_questions = [question[0] for question in cur.fetchall()]

        # Close the cursor and database connection
        cur.close()
        con.close()

        return module1_questions

    # Fetch questions from module 1 in the database
    module1_questions = fetch_module1_questions()

    # Create checkboxes for each question from Module 1
    for index, question in enumerate(module1_questions, start=1):
        checkbox = tk.Checkbutton(frame, text=question, command=lambda q=question: toggle_question(q))
        checkbox.pack(anchor=tk.W)

    # Define function to add selected questions to qpmod1
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
        query = "INSERT INTO qpmod1 (questions) VALUES (%s)"

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
        messagebox.showinfo("Success", "Selected questions have been added to qpmod1.")

    # Add button to add selected questions to qpmod1
    add_button = tk.Button(root, text="Add", command=add_questions)
    add_button.pack(pady=10)

    # Define function to open window for adding questions from Module 2
    def add_module2_questions():
        createqpmod2.create_qp_mod2(root,window_manager)
        root.destroy()

    # Add button to add questions from Module 2
    add_module2_button = tk.Button(root, text="Add Questions To Module 2", command=add_module2_questions)
    add_module2_button.pack(pady=10)
    window_manager.add_window(root)
    root.mainloop()
