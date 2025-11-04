from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from datetime import datetime
from werkzeug.utils import secure_filename
from subject_config import SUBJECTS
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import make_response
import io
from flask import send_file


app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/notes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BRANCH_PASSWORDS = {
    'csd': 'csd123',
    'aiml': 'aiml123',
    'data_science': 'ds123',
    'civil': 'civil123',
    'biomedical': 'bio123'
}

# ---------- DB FUNCTIONS ----------
def get_db_name(semester):
    return f'sem{semester}.db'

def ensure_marks_table(semester):
    db_name = get_db_name(semester)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    columns = """
        username TEXT PRIMARY KEY
    """
    for i in range(1, 7):
        for ia in ['IA1', 'IA2', 'IA3']:
            columns += f", sub{i}_{ia} TEXT"
        columns += f", sub{i}_classes_held TEXT, sub{i}_classes_attended TEXT"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS marks ({columns})")
    con.commit()
    con.close()

# ---------- LOGIN HELPERS ----------
def log_login(username, role):
    con = sqlite3.connect('logins.db')
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("INSERT INTO logins (username, role, timestamp) VALUES (?, ?, ?)", 
                   (username, role, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    con.commit()
    con.close()

def validate_user(db, username, password):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

# ---------- ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('students.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))
        student = cursor.fetchone()
        con.close()
        if student:
            session.clear()
            session['user'] = username
            session['role'] = 'student'
            session['name'] = student[3]
            session['branch'] = student[4]
            session['year'] = student[5]
            session['semester'] = student[6]
            session['usn'] = password
            log_login(username, 'student')
            return redirect(url_for('student_dashboard'))
        flash("Invalid credentials")
    return render_template('student_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('student_login'))
    
    semester = session['semester']
    username = session['user']
    db_name = get_db_name(semester)

    student_data = {}
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM marks WHERE username=?", (username,))
        data = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        student_data = dict(zip(columns, data)) if data else {}
        con.close()
    except Exception as e:
        print("Error loading student marks:", e)

    return render_template('student_dashboard.html', name=session['name'], usn=session['usn'], data=student_data)


@app.route('/view_marks')
def view_marks():
    if session.get('role') != 'student':
        return redirect(url_for('student_login'))

    semester = session['semester']
    branch = session['branch']
    username = session['user']
    db_name = f'sem{semester}.db'

    # Get student marks
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM marks WHERE username=?", (username,))
    data = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    con.close()

    if data:
        student_data = dict(zip(columns, data))
        from subject_config import SUBJECTS
        subjects = SUBJECTS.get(branch, {}).get(semester, [])

        return render_template('view_marks.html', data=student_data, subjects=subjects)
    else:
        flash("No marks data available.")
        return redirect(url_for('student_dashboard'))
    
@app.route('/download_marksheet')
def download_marksheet():
    if session.get('role') != 'student':
        return redirect(url_for('student_login'))

    semester = session['semester']
    branch = session['branch']
    username = session['user']
    db_name = f'sem{semester}.db'

    # Fetch student marks
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM marks WHERE username=?", (username,))
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    con.close()

    if not row:
        flash("No marks found.")
        return redirect(url_for('student_dashboard'))

    data = dict(zip(columns, row))
    subjects = SUBJECTS.get(branch, {}).get(semester, [])

    # PDF generation
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Heading
    story.append(Paragraph("<b>Academic Marksheet / Certificate</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Name:</b> {session['name']}", styles['Normal']))
    story.append(Paragraph(f"<b>USN:</b> {session['usn']}", styles['Normal']))
    story.append(Paragraph(f"<b>Branch:</b> {branch.capitalize()} | <b>Semester:</b> {semester}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Table Data
    table_data = [['Subject Code', 'Subject Name', 'IA1', 'IA2', 'IA3']]
    for i, subject in enumerate(subjects, start=1):
        code, name = subject
        ia1 = data.get(f'sub{i}_ia1', '-')
        ia2 = data.get(f'sub{i}_ia2', '-')
        ia3 = data.get(f'sub{i}_ia3', '-')
        table_data.append([code, name, ia1, ia2, ia3])

    t = Table(table_data, colWidths=[80, 200, 50, 50, 50])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(t)

    doc.build(story)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="marksheet.pdf", mimetype='application/pdf')



@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('teachers.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM teachers WHERE username=? AND password=?", (username, password))
        teacher = cursor.fetchone()
        con.close()
        if teacher:
            session.clear()
            session['user'] = username
            session['role'] = 'teacher'
            log_login(username, 'teacher')
            return redirect(url_for('select_branch'))
        flash("Invalid teacher credentials")
    return render_template('teacher_login.html')

@app.route('/select_branch')
def select_branch():
    if session.get('role') != 'teacher':
        return redirect(url_for('teacher_login'))
    return render_template('select_branch.html')

@app.route('/branch_login/<branch>', methods=['GET', 'POST'])
def branch_login(branch):
    if session.get('role') != 'teacher':
        return redirect(url_for('teacher_login'))
    if request.method == 'POST':
        if request.form['password'] == BRANCH_PASSWORDS.get(branch):
            session['branch_access'] = branch
            return redirect(url_for('branch_dashboard', branch=branch))
        flash("Incorrect branch password")
    return render_template('branch_password.html', branch=branch)

@app.route('/branch_dashboard/<branch>')
def branch_dashboard(branch):
    if session.get('branch_access') != branch:
        return redirect(url_for('branch_login', branch=branch))
    return render_template('branch_dashboard.html', branch=branch)

@app.route('/branch_semester/<branch>/<int:year>/<int:semester>', methods=['GET', 'POST'])
def branch_semester(branch, year, semester):
    if session.get('branch_access') != branch:
        return redirect(url_for('branch_login', branch=branch))

    db_name = f'sem{semester}.db'

    # Get students
    con = sqlite3.connect('students.db')
    cursor = con.cursor()
    cursor.execute("SELECT username FROM students WHERE branch=? AND year=? AND semester=?", 
                   (branch, year, semester))
    students = [s[0] for s in cursor.fetchall()]
    con.close()

    subjects = SUBJECTS.get(branch, {}).get(semester, [])

    ia_type = request.form.get("ia_type") or request.args.get("ia_type") or "ia1"
    data = {}

    if request.method == 'POST' and request.form.get("student"):
        student = request.form['student']
        action = request.form.get('action')

        con_sem = sqlite3.connect(db_name)
        cursor_sem = con_sem.cursor()

        if action == 'reset':
            for i in range(1, 7):
                cursor_sem.execute(f"""
                    UPDATE marks SET 
                        sub{i}_{ia_type} = NULL,
                        sub{i}_att{ia_type[-1]} = NULL
                    WHERE username = ?
                """, (student,))
        elif action == 'save':
            values = []
            for i in range(1, 7):
                marks = request.form.get(f'sub{i}_marks', '')
                att = request.form.get(f'sub{i}_attended', '')
                values.extend([marks, att])
            sql = f"""
                INSERT INTO marks (username, {', '.join([f'sub{i}_{ia_type}, sub{i}_att{ia_type[-1]}' for i in range(1,7)] )})
                VALUES (?, {', '.join(['?']*12)})
                ON CONFLICT(username) DO UPDATE SET
                {', '.join([f'sub{i}_{ia_type} = excluded.sub{i}_{ia_type}, sub{i}_att{ia_type[-1]} = excluded.sub{i}_att{ia_type[-1]}' for i in range(1,7)])}
            """
            cursor_sem.execute(sql, (student, *values))

        con_sem.commit()
        con_sem.close()
        return redirect(url_for('branch_semester', branch=branch, year=year, semester=semester, ia_type=ia_type))

    # Get current data to pre-fill
    con_sem = sqlite3.connect(db_name)
    cursor_sem = con_sem.cursor()
    for student in students:
        cursor_sem.execute("SELECT * FROM marks WHERE username = ?", (student,))
        row = cursor_sem.fetchone()
        if row:
            columns = [desc[0] for desc in cursor_sem.description]
            data[student] = dict(zip(columns, row))
        else:
            data[student] = None
    con_sem.close()

    return render_template('branch_semester.html', branch=branch, year=year, semester=semester,
                           students=students, subjects=subjects, data=data, ia_type=ia_type)

@app.route('/view_notes')
def view_notes():
    if 'user' not in session or session.get('role') != 'student':
        return redirect(url_for('student_login'))

    branch = session.get('branch')
    year = session.get('year')
    semester = session.get('semester')

    notes_path = os.path.join(app.config['UPLOAD_FOLDER'], branch, f'year{year}_sem{semester}')
    notes = {}

    if os.path.exists(notes_path):
        for subject in os.listdir(notes_path):
            subject_path = os.path.join(notes_path, subject)
            if os.path.isdir(subject_path):
                notes[subject] = {}
                for module in os.listdir(subject_path):
                    module_path = os.path.join(subject_path, module)
                    if os.path.isdir(module_path):
                        notes[subject][module] = os.listdir(module_path)

    return render_template('view_notes.html', notes=notes, branch=branch, year=year, semester=semester)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if session.get('role') != 'teacher':
        return redirect(url_for('teacher_login'))

    if request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        branch = request.form['branch']
        year = request.form['year']
        semester = request.form['semester']

        username = name.strip().lower().replace(" ", "_")
        password = usn.strip()

        con = sqlite3.connect('students.db')
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                name TEXT,
                branch TEXT,
                year INTEGER,
                semester INTEGER
            )
        """)

        # ✅ Check for same USN within the same branch
        cursor.execute("SELECT * FROM students WHERE password=? AND branch=?", (password, branch))
        if cursor.fetchone():
            flash("A student with this USN already exists in this branch.")
            con.close()
            return render_template('add_student.html')

        try:
            cursor.execute("""
                INSERT INTO students (username, password, name, branch, year, semester)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password, name, branch, year, semester))
            con.commit()
            flash("Student added successfully!")
        except sqlite3.IntegrityError:
            flash("A student with this username already exists.")
        finally:
            con.close()

    return render_template('add_student.html')    

@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if session.get('role') != 'teacher':
        return redirect(url_for('teacher_login'))

    con = sqlite3.connect('students.db')
    cursor = con.cursor()
    cursor.execute("SELECT name, password, branch, year, semester FROM students")
    students = cursor.fetchall()
    con.close()

    if request.method == 'POST':
        usn = request.form['usn']
        branch = request.form['branch']

        con = sqlite3.connect('students.db')
        cursor = con.cursor()
        cursor.execute("DELETE FROM students WHERE password=? AND branch=?", (usn, branch))
        con.commit()
        con.close()

        flash("Student deleted successfully.")
        return redirect(url_for('delete_student'))

    return render_template('delete_student.html', students=students)


@app.route('/upload_notes/<branch>/<int:year>/<int:semester>', methods=['GET', 'POST'], endpoint='upload_notes_teacher')
def upload_notes_teacher(branch, year, semester):
    if session.get('role') != 'teacher' or session.get('branch_access') != branch:
        return redirect(url_for('teacher_login'))

    # Get subjects from subject_config.py
    from subject_config import SUBJECTS
    subjects = SUBJECTS.get(branch, {}).get(semester, [])

    if request.method == 'POST':
        subject = request.form['subject']
        module = request.form['module']
        file = request.files['file']

        if file and subject and module:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], branch, f'year{year}_sem{semester}', subject, module)
            os.makedirs(path, exist_ok=True)
            file.save(os.path.join(path, filename))
            flash("Note uploaded successfully!")
            return redirect(url_for('upload_notes_teacher', branch=branch, year=year, semester=semester))
        else:
            flash("All fields are required!")

    return render_template('upload_notes.html', branch=branch, year=year, semester=semester, subjects=subjects)

@app.route('/logout')
def logout():
    role = session.get('role')
    session.clear()
    if role == 'teacher':
        return redirect(url_for('select_branch'))
    else:
        return redirect(url_for('index'))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
