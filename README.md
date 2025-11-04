# 🎓 Student and Teacher Web Portal

A web application built using **Flask** that serves as a portal for students and teachers.

- 👩‍🏫 Teachers can **log in**, **enter attendance**, and **upload marks** for each student by branch and semester.
- 👨‍🎓 Students can **log in using their name and USN**, view their **attendance**, **marks**, **semester reports**, and **download mark sheets**.

---

## 📂 Features

### 🧑‍🏫 Teacher Portal
- Secure login with pre-defined credentials.
- Enter and update:
  - Student marks
  - Student attendance
- Select branch and semester to manage specific student data.

### 🎓 Student Portal
- Login using:
  - Username: Student's Name
  - Password: Student's USN
- View:
  - Marks per subject
  - Attendance percentage
  - Semester report
- Download PDF mark sheets.

### 🗃️ Database
- Stores:
  - Student details
  - Attendance
  - Marks
  - Semester-wise data
- Unique login per student (Name + USN).

---

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **SQLite** (or any other DB used)
- **HTML/CSS**
- **Bootstrap** (optional, for styling)
- **Jinja2** (for templates)

---

## 🚀 How to Run the Project

### 1. Clone the Repository

``bash
git clone 
cd student-teacher-portal
2. Create Virtual Environment (Optional but Recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
If requirements.txt is not present, install Flask manually:

bash
Copy code
pip install Flask
4. Run the Flask App
bash
Copy code
python app.py
The app will start on:

cpp
Copy code
http://127.0.0.1:5000
🔐 Default Login Credentials
🧑‍🏫 Teacher Login
Set inside the code in a dictionary or configuration file

Username: teacher1

Password: password123

You can modify/add more teachers in the code.

🎓 Student Login
Username: Student's Name (e.g., John Doe)

Password: Student's USN (e.g., 1RV20CS001)

These credentials are provided by the teacher when adding the student into the portal.

📌 Notes
Ensure the database (students.db) is correctly set up with tables for:

Students

Marks

Attendance

Use a separate admin interface or DB scripts to populate initial data if needed.

You can enhance the project with:

Graphical dashboards

Export options (PDF, Excel)

Email notifications
