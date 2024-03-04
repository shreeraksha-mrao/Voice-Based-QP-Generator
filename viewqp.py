import tkinter as tk
from tkinter import messagebox
import mysql.connector
from closeall import WindowManager
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
    )
    cur = con.cursor()

    # Create a PDF document
    pdf_filename = "question_paper.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Define a style for the questions
    styles = getSampleStyleSheet()
    question_style = styles["Normal"]

    # Create a list of elements to add to the PDF
    elements = []

    # Add the title, scheme, semester, subject, time, and max marks
    title = "FIFTH SEMESTER B.E EXAMINATION"
    scheme = "CSBS SCHEME"
    semester = "NOTE:- ANSWER ANY ONE SUBSECTION OF QUESTIONS FROM EACH MODULE"
    subject = "SUBJECT: AIML"
    time_and_marks = "Time: 3 hrs                                       Max Marks: 100"

    
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(scheme, styles["Normal"]))
    elements.append(Paragraph(semester, styles["Normal"]))
    elements.append(Paragraph(subject, styles["Normal"]))
    elements.append(Paragraph(time_and_marks, styles["Normal"]))  # Combine time and max marks in one paragraph
    elements.append(Spacer(1, 24))  # Add space between header and questions

    
    def generate_pdf():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
    )
    cur = con.cursor()

    # Create a PDF document
    pdf_filename = "question_paper.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Define a style for the questions
    styles = getSampleStyleSheet()
    question_style = styles["Normal"]

    # Create a list of elements to add to the PDF
    elements = []

    # Add the title, scheme, semester, subject, time, and max marks
    title = "FIFTH SEMESTER B.E EXAMINATION"
    scheme = "CSBS SCHEME"
    semester = "NOTE:- ANSWER ANY ONE SUBSECTION OF QUESTIONS FROM EACH MODULE"
    subject = "SUBJECT: AIML"
    time_and_marks = "Time: 3 hrs                                       Max Marks: 100"

    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(scheme, styles["Normal"]))
    elements.append(Paragraph(semester, styles["Normal"]))
    elements.append(Paragraph(subject, styles["Normal"]))
    elements.append(Paragraph(time_and_marks, styles["Normal"]))  # Combine time and max marks in one paragraph
    elements.append(Spacer(1, 24))  # Add space between header and questions

    for i in range(1, 6):
        cur.execute(f"SELECT questions, marks FROM qpmod{i}")  # Execute the query
        questions_result = cur.fetchall()  # Fetch the results
        questions = [(row[0], row[1]) for row in questions_result]  # Extract the questions and marks from the result

        elements.append(Paragraph(f"Module {i}", styles["Heading1"]))
        page_width = letter[0]
        fixed_width = page_width * 0.8

        col_width = fixed_width

        num_questions = 8

        # Divide the questions into two groups of 4 each
        group1 = questions[:4]
        group2 = questions[4:8]

        # Create the first table for the first group of questions
        table_data = []
        for j, (question, marks) in enumerate(group1, start=1):
            table_data.append([f"{j}) {question} (Marks: {marks})"])

        question_table = Table(table_data, colWidths=[col_width])
        question_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONT_SIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(question_table)

        # Add "OR" text
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("OR", styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Create the second table for the second group of questions
        table_data = []
        for j, (question, marks) in enumerate(group2, start=5):  # Start numbering from 5 for the second group
            table_data.append([f"{j}) {question} (Marks: {marks})"])

        question_table = Table(table_data, colWidths=[col_width])
        question_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONT_SIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(question_table)
        elements.append(Spacer(1, 24))

    con.close()
    doc.build(elements)


    
    
    
def display_questions_qp(parent):
    generate_pdf()
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
    )
    cur = con.cursor()

    global root  # Make root global so it can be accessed from go_back function

    root = tk.Tk()
    root.title("View Question Paper")
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
        cur.execute(f"SELECT questions FROM qpmod{module_number}")
        questions = cur.fetchall()
        if questions:
            label_module = tk.Label(inner_frame, text=f"Module {module_number} Questions:", font=('Arial', 12, 'bold'))
            label_module.pack(pady=(10, 5), anchor="w")  # Add padding between modules and left align
            for index, question in enumerate(questions, start=1):
                label_question = tk.Label(inner_frame, text=f"{index}. {question[0]}", anchor="w")
                label_question.pack(fill=tk.X)  # Expand label horizontally to fill the width

    # Create a frame for the right side (color bar) and pack it to the right
    right_frame = tk.Frame(main_frame, width=500, bg="#FFC0CB")  # Pink color
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Add a label for the download message and pack it to the bottom
    label_download = tk.Label(root, text="Question paper in required format downloaded into your system", font=('Arial', 14, 'bold'))
    label_download.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  # Center align

    def close_window():  # Function to close the window and resurface MyGui2
        root.destroy()
        parent.deiconify()

    # Add a "Go Back" button and pack it to the bottom
    btn_go_back = tk.Button(root, text="Go Back", command=close_window)
    btn_go_back.pack(side=tk.BOTTOM, pady=10)  # Center align

    con.close()

    root.mainloop()
    
