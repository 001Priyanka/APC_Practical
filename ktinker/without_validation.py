import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def handle_submission():
    # Directly collect field data without checking for errors or empty spaces
    fullname = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    gender = gender_var.get()
    course = course_combobox.get()
    
    # Directly trigger the success popup box
    success_msg = f"Registration Received!\n\nName: {fullname}\nEmail: {email}\nPhone: {phone}\nGender: {gender}\nCourse: {course}"
    messagebox.showinfo("Success", success_msg)
    
    # Reset form fields
    clear_form()

def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    gender_var.set("Not Selected")
    course_combobox.set("")

# --- UI SETUP ---
root = tk.Tk()
root.title("Simple Student Registration Form")
root.geometry("450x400")
root.configure(bg="#f4f4f9")

# Content layout frame
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, borderwidth=1, relief="solid")
frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=360)

# Form Header label
header = tk.Label(frame, text="Student Registration", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333")
header.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Field Titles
labels_text = ["Full Name:", "Email Address:", "Phone Number:", "Gender:", "Course:"]
for i, txt in enumerate(labels_text):
    lbl = tk.Label(frame, text=txt, font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#555555")
    lbl.grid(row=i+1, column=0, sticky="w", pady=8)

# Input Entry widgets
name_entry = tk.Entry(frame, font=("Helvetica", 10), width=25)
name_entry.grid(row=1, column=1, pady=8, sticky="w")

email_entry = tk.Entry(frame, font=("Helvetica", 10), width=25)
email_entry.grid(row=2, column=1, pady=8, sticky="w")

phone_entry = tk.Entry(frame, font=("Helvetica", 10), width=25)
phone_entry.grid(row=3, column=1, pady=8, sticky="w")

# Gender Choice Radiobuttons
gender_var = tk.StringVar(value="Not Selected")
gender_frame = tk.Frame(frame, bg="#ffffff")
gender_frame.grid(row=4, column=1, pady=8, sticky="w")

rb_male = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg="#ffffff")
rb_male.pack(side="left", padx=5) 
rb_female = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg="#ffffff")
rb_female.pack(side="left", padx=5)

# Course Dropdown options
course_combobox = ttk.Combobox(frame, font=("Helvetica", 10), width=23, state="readonly")
course_combobox['values'] = ("Computer Science", "Information Technology", "Data Science", "Mechanical Engineering", "Business Analytics")
course_combobox.grid(row=5, column=1, pady=8, sticky="w")

# Action trigger button
submit_btn = tk.Button(frame, text="Submit Registration", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", 
                       activebackground="#45a049", activeforeground="white", cursor="hand2", command=handle_submission)
submit_btn.grid(row=6, column=0, columnspan=2, pady=(20, 0))

root.mainloop()
