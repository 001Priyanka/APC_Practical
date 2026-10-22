import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

# --- VALIDATION FUNCTIONS ---
def validate_email(email):
    # Basic regex validation for standard email layout
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_phone(phone):
    # Ensures phone number is exactly 10 numeric digits
    return phone.isdigit() and len(phone) == 10

def handle_submission():
    # Retrieve field data
    fullname = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    gender = gender_var.get()
    course = course_combobox.get()
    
    # 1. Check for empty fields
    if not fullname or not email or not phone or gender == "Not Selected" or not course:
        messagebox.showerror("Validation Error", "All fields are required! Please fill out the entire form.")
        return

    # 2. Check for Name validity (text only)
    if not all(x.isalpha() or x.isspace() for x in fullname):
        messagebox.showerror("Validation Error", "Name must contain letters and spaces only.")
        return

    # 3. Check for Email validity
    if not validate_email(email):
        messagebox.showerror("Validation Error", "Please enter a valid email address (e.g., name@example.com).")
        return

    # 4. Check for Phone validity
    if not validate_phone(phone):
        messagebox.showerror("Validation Error", "Phone number must be exactly 10 digits and numbers only.")
        return

    # If all validations pass, show success message box
    success_msg = f"Registration Successful!\n\nName: {fullname}\nEmail: {email}\nPhone: {phone}\nGender: {gender}\nCourse: {course}"
    messagebox.showinfo("Success", success_msg)
    
    # Reset form after submission
    clear_form()

def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    gender_var.set("Not Selected")
    course_combobox.set("")

# --- UI SETUP ---
# Initialize main application window
root = tk.Tk()
root.title("Student Registration Form")
root.geometry("450x400")
root.configure(bg="#f4f4f9")

# Set up form frame
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, borderwidth=1, relief="solid")
frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=360)

# Form Header
header = tk.Label(frame, text="Student Registration", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333")
header.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Fields Configuration Layout
labels_text = ["Full Name:", "Email Address:", "Phone Number:", "Gender:", "Course:"]
for i, txt in enumerate(labels_text):
    lbl = tk.Label(frame, text=txt, font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#555555")
    lbl.grid(row=i+1, column=0, sticky="w", pady=8)

# Input Widgets
name_entry = tk.Entry(frame, font=("Helvetica", 10), width=25)
name_entry.grid(row=1, column=1, pady=8, sticky="w")

email_entry = tk.Entry(frame, font=("Helvetica", 10), width=25)
email_entry.grid(row=2, column=1, pady=8, sticky="w")

phone_entry = tk.Entry(frame, font=("Helvetica", 10), width=25)
phone_entry.grid(row=3, column=1, pady=8, sticky="w")

# Gender Radio Buttons Container
gender_var = tk.StringVar(value="Not Selected")
gender_frame = tk.Frame(frame, bg="#ffffff")
gender_frame.grid(row=4, column=1, pady=8, sticky="w")

rb_male = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg="#ffffff")
rb_male.pack(side="left", padx=5)
rb_female = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg="#ffffff")
rb_female.pack(side="left", padx=5)

# Course Dropdown Selection
course_combobox = ttk.Combobox(frame, font=("Helvetica", 10), width=23, state="readonly")
course_combobox['values'] = ("Computer Science", "Information Technology", "Data Science", "Mechanical Engineering", "Business Analytics")
course_combobox.grid(row=5, column=1, pady=8, sticky="w")

# Submit Action Button
submit_btn = tk.Button(frame, text="Submit Registration", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", 
                       activebackground="#45a049", activeforeground="white", cursor="hand2", command=handle_submission)
submit_btn.grid(row=6, column=0, columnspan=2, pady=(20, 0))

# Start the application loop
root.mainloop()
