import tkinter as tk
import speech_recognition as sr
import mysql.connector
from closeall import WindowManager

def add_to_existing_questionbank(parent):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
    )
    cur = con.cursor()

    root = tk.Toplevel(parent)  # Use the top-level window reference passed from MyGui2
    root.title("Question Bank Management")
    root.attributes('-fullscreen', True)  # Make the window fullscreen


    def speech():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                question = r.recognize_google(audio)
                label_var.set(f"The question is: {question}")
                return question

            except sr.UnknownValueError:
                label_var.set("Sorry, I could not understand that.")
                return "-1"

            except sr.RequestError as e:
                label_var.set(f"Error: Could not request results; {e}")
                return "-1"

    def add_question_gui(module_number):
        label_var.set("Speak up your question...")  # Set the label to "Speak up your question..."
        root.update()  # Update the GUI to show the "Speak up your question..." message

        question = speech()  # Call the speech recognition function

        if question == "-1":
            label_var.set("Try again")  # Set the label to "Try again" if recognition fails
            root.update()  # Update the GUI to show the "Try again" message
            question = speech()  # Call the speech recognition function again

        if question != "-1":
            cur.execute(f"INSERT INTO module{module_number} (module_{module_number}_questions) VALUES ('{question}')")
            con.commit()
            label_var.set(f"The question is: {question}\nQuestion added successfully to module {module_number}")  # Set the label to the recognized question and success message

    def close_window():  # Function to close the window and resurface MyGui2
        root.destroy()
        parent.deiconify()

    label_var = tk.StringVar()
    label_var.set("")

    frame = tk.Frame(root)
    frame.pack()

    tk.Label(frame, text="Select Module:").pack()

    module_var = tk.IntVar()
    module_var.set(1)

    for i in range(1, 6):
        tk.Radiobutton(frame, text=f"Module {i}", variable=module_var, value=i).pack(side=tk.TOP, anchor='center')


    tk.Button(frame, text="Add Question", command=lambda: add_question_gui(module_var.get())).pack()
    tk.Label(frame, textvariable=label_var).pack()

    # Add close button
    tk.Button(root, text="Go Backk", command=close_window).pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
