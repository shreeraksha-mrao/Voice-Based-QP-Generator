import tkinter as tk
from tkinter import messagebox
import mysql.connector
from closeall import WindowManager

def display_questions(parent):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
    )
    cur = con.cursor()

    global root  # Make root global so it can be accessed from go_back function

    root = tk.Tk()
    root.title("View Question Bank")
    root.attributes('-fullscreen', True)  # Open in full screen

    # Create main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the left side (questions) and pack it to the left
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a canvas with scrollbar
    canvas = tk.Canvas(left_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind the canvas to the scrollbar
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame to contain the labels inside the canvas
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Fetch questions from each module
    for module_number in range(1, 6):
        cur.execute(f"SELECT module_{module_number}_questions FROM module{module_number}")
        questions = cur.fetchall()
        if questions:
            label_module = tk.Label(inner_frame, text=f"Module {module_number} Questions:", font=('Arial', 12, 'bold'))
            label_module.pack(pady=(10, 5), anchor="w")  # Add padding between modules and left align
            for index, question in enumerate(questions, start=1):
                label_question = tk.Label(inner_frame, text=f"{index}. {question[0]}", anchor="w")
                label_question.pack(fill=tk.X)  # Expand label horizontally to fill the width

    # Create a frame for the right side (color bar) and pack it to the right
    right_frame = tk.Frame(main_frame, width=500, bg="#FFFF00")  # Yellow color
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    def close_window():  # Function to close the window and resurface MyGui2
        root.destroy()
        parent.deiconify()

    # Add a "Go Back" button and pack it to the bottom
    btn_go_back = tk.Button(root, text="Go Back", command=close_window)
    btn_go_back.pack(side=tk.BOTTOM, pady=10)  # Center align

    con.close()

    root.mainloop()

