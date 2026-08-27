
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import os
import sqlite3


# =========================================================
# APP
# =========================================================

app = Flask(__name__)

app.secret_key = "college_portal_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# STUDENT TABLE
# =========================================================

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    roll_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    class_name = db.Column(
        db.String(50),
        nullable=False
    )

    year = db.Column(
        db.String(30),
        nullable=False,
        default="3rd Year"
    )

    batch = db.Column(
        db.String(30),
        nullable=False,
        default="2024-2028"
    )

    department = db.Column(
        db.String(100),
        nullable=False,
        default="Computer Science and Engineering"
    )

    attendance_records = db.relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    marks_records = db.relationship(
        "Marks",
        back_populates="student",
        cascade="all, delete-orphan"
    )


# =========================================================
# TEACHER TABLE
# =========================================================

class Teacher(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    subject = db.Column(
        db.String(100),
        nullable=False
    )

    attendance_records = db.relationship(
        "Attendance",
        back_populates="teacher"
    )


# =========================================================
# ADMIN TABLE
# =========================================================

class Admin(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )


# =========================================================
# ATTENDANCE TABLE
# =========================================================

class Attendance(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    subject = db.Column(
        db.String(100),
        nullable=False
    )

    attendance_date = db.Column(
        db.String(20),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher.id"),
        nullable=False
    )

    student = db.relationship(
        "Student",
        back_populates="attendance_records"
    )

    teacher = db.relationship(
        "Teacher",
        back_populates="attendance_records"
    )


# =========================================================
# MARKS TABLE
# =========================================================

class Marks(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    subject = db.Column(
        db.String(100),
        nullable=False
    )

    internal = db.Column(
        db.Integer,
        nullable=False
    )

    external = db.Column(
        db.Integer,
        nullable=False
    )

    student = db.relationship(
        "Student",
        back_populates="marks_records"
    )


# =========================================================
# STUDENT DATA
# =========================================================
#
# IMPORTANT:
# Paste your EXISTING students_data list here.
# Do not change the names/passwords.
#
# Example:
#
# students_data = [
#     ("Y24CSE279001", "Abdul Sajida", "sajida001", "279001", "CSE-A"),
#     ...
# ]
#
# Use the complete list you already have.
# =========================================================

students_data = [

    # PASTE YOUR COMPLETE EXISTING students_data HERE

]


# =========================================================
# ORIGINAL 13 TEACHERS
# =========================================================

teachers_data = [

    ("SOMU", "somu", "somu@", "CN"),

    ("ABIDA BEGUM", "begum", "begum@", "NILL"),

    ("SALMA BEGUM", "salma", "salma@", "PE-1"),

    ("BHAVANI SHANKAR", "shankar", "shankar@", "NILL"),

    ("PRINCIPAL(OOAD)", "principal", "principal@", "OOAD"),

    ("RAJEEV", "rajeev", "rajeev@", "WCS"),

    ("ALI MIRZA", "ali", "ali@", "DW&DM"),

    ("KAVITHA", "kavitha", "kavitha@", "NILL"),

    ("ROJA", "roja", "roja@", "NILL"),

    ("RANGASREE", "rangasree", "rangasree@", "NILL"),

    ("RAGAV NAIDU", "naidu", "naidu@", "NILL"),

    ("K.G.V.K", "krishna", "krishna@", "NILL"),

    ("BALAJI", "balaji", "balaji@", "NILL"),

]


# =========================================================
# ORIGINAL ATTENDANCE DATA
# =========================================================
#
# Paste your COMPLETE existing ORIGINAL_ATTENDANCE dictionary
# here exactly as you already have it.
# =========================================================

ORIGINAL_ATTENDANCE = {

    # PASTE YOUR COMPLETE EXISTING ORIGINAL_ATTENDANCE HERE

}


# =========================================================
# DATABASE SCHEMA FIX
# =========================================================

def fix_old_database():

    """
    SQLAlchemy db.create_all() does not modify an existing table.

    If the old database was created before year/batch/department
    were added, this function adds the missing columns.
    """

    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "database.db"
    )

    if not os.path.exists(db_path):
        return

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:

        # -----------------------------------------------------
        # STUDENT TABLE
        # -----------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(student)"
        )

        student_columns = {
            row[1]
            for row in cursor.fetchall()
        }

        if "year" not in student_columns:

            cursor.execute(
                """
                ALTER TABLE student
                ADD COLUMN year VARCHAR(30)
                """
            )

            cursor.execute(
                """
                UPDATE student
                SET year = '3rd Year'
                WHERE year IS NULL
                """
            )

        if "batch" not in student_columns:

            cursor.execute(
                """
                ALTER TABLE student
                ADD COLUMN batch VARCHAR(30)
                """
            )

            cursor.execute(
                """
                UPDATE student
                SET batch = '2024-2028'
                WHERE batch IS NULL
                """
            )

        if "department" not in student_columns:

            cursor.execute(
                """
                ALTER TABLE student
                ADD COLUMN department VARCHAR(100)
                """
            )

            cursor.execute(
                """
                UPDATE student
                SET department =
                'Computer Science and Engineering'
                WHERE department IS NULL
                """
            )

        # -----------------------------------------------------
        # ATTENDANCE TABLE
        # -----------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(attendance)"
        )

        attendance_columns = {
            row[1]
            for row in cursor.fetchall()
        }

        if "teacher_id" not in attendance_columns:

            cursor.execute(
                """
                ALTER TABLE attendance
                ADD COLUMN teacher_id INTEGER
                """
            )

        connection.commit()

    except Exception as error:

        print(
            "Database schema check:",
            error
        )

    finally:

        connection.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    db.create_all()

    # =====================================================
    # FIX OLD DATABASE
    # =====================================================

    fix_old_database()

    # =====================================================
    # CREATE / UPDATE 13 TEACHERS
    # =====================================================

    for name, username, password, subject in teachers_data:

        teacher = Teacher.query.filter_by(
            username=username
        ).first()

        if teacher is None:

            teacher = Teacher(
                name=name,
                username=username,
                password=password,
                subject=subject
            )

            db.session.add(teacher)

        else:

            teacher.name = name
            teacher.password = password
            teacher.subject = subject

    # =====================================================
    # ADMIN
    # =====================================================

    admin = Admin.query.filter_by(
        username="admin001"
    ).first()

    if admin is None:

        admin = Admin(
            username="admin001",
            password="admin001"
        )

        db.session.add(admin)

    # =====================================================
    # STUDENTS
    # =====================================================

    for roll_number, name, username, password, class_name in students_data:

        student = Student.query.filter_by(
            roll_number=roll_number
        ).first()

        if student is None:

            student = Student(
                roll_number=roll_number,
                name=name,
                username=username,
                password=password,
                class_name=class_name,
                year="3rd Year",
                batch="2024-2028",
                department="Computer Science and Engineering"
            )

            db.session.add(student)

        else:

            student.name = name
            student.username = username
            student.password = password
            student.class_name = class_name
            student.year = "3rd Year"
            student.batch = "2024-2028"
            student.department = "Computer Science and Engineering"

    db.session.commit()


# =========================================================
# IMPORT ORIGINAL ATTENDANCE
# =========================================================

def import_original_attendance():

    teacher = Teacher.query.filter_by(
        username="somu"
    ).first()

    if teacher is None:
        return

    if not ORIGINAL_ATTENDANCE:
        return

    subject = "Regular Classes"

    for attendance_date, sections in ORIGINAL_ATTENDANCE.items():

        for section, present_numbers in sections.items():

            if section == "A":
                class_name = "CSE-A"
            else:
                class_name = "CSE-B"

            students = Student.query.filter_by(
                class_name=class_name
            ).all()

            for student in students:

                try:

                    number = int(
                        student.roll_number[-3:]
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    continue

                if number in present_numbers:

                    status = "Present"

                else:

                    status = "Absent"

                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    subject=subject,
                    attendance_date=attendance_date
                ).first()

                if existing is None:

                    record = Attendance(
                        student_id=student.id,
                        subject=subject,
                        attendance_date=attendance_date,
                        status=status,
                        teacher_id=teacher.id
                    )

                    db.session.add(record)

                else:

                    existing.status = status
                    existing.teacher_id = teacher.id

    db.session.commit()


# =========================================================
# START DATABASE
# =========================================================

with app.app_context():

    initialize_database()

    import_original_attendance()


# =========================================================
# STUDENT LOGIN PAGE
# =========================================================

@app.route("/")
def login():

    return render_template(
        "login.html"
    )


# =========================================================
# STUDENT LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["POST"]
)
def do_login():

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    ).strip()

    student = Student.query.filter_by(
        username=username
    ).first()

    if student is None:

        return "Username not found"

    if student.password != password:

        return "Password is incorrect"

    session.clear()

    session["student_id"] = student.id

    return redirect(
        "/dashboard"
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    student_id = session.get(
        "student_id"
    )

    if not student_id:

        return redirect("/")

    student = db.session.get(
        Student,
        student_id
    )

    if student is None:

        session.clear()

        return redirect("/")

    return render_template(
        "dashboard.html",
        student=student
    )


# =========================================================
# STUDENT PROFILE
# =========================================================

@app.route("/profile")
def profile():

    student_id = session.get(
        "student_id"
    )

    if not student_id:

        return redirect("/")

    student = db.session.get(
        Student,
        student_id
    )

    if student is None:

        session.clear()

        return redirect("/")

    return render_template(
        "profile.html",
        student=student
    )


# =========================================================
# STUDENT ATTENDANCE
# =========================================================

@app.route("/attendance")
def attendance():

    student_id = session.get(
        "student_id"
    )

    if not student_id:

        return redirect("/")

    student = db.session.get(
        Student,
        student_id
    )

    if student is None:

        session.clear()

        return redirect("/")

    attendance_records = Attendance.query.filter_by(
        student_id=student.id
    ).all()

    # -----------------------------------------------------
    # SORT ATTENDANCE BY DATE
    # -----------------------------------------------------

    def sort_date(record):

        try:

            return datetime.strptime(
                record.attendance_date,
                "%d-%m-%Y"
            )

        except (
            ValueError,
            TypeError
        ):

            return datetime.min

    attendance_records.sort(
        key=sort_date
    )

    # -----------------------------------------------------
    # SUBJECT-WISE ATTENDANCE
    # -----------------------------------------------------

    subjects = {}

    for record in attendance_records:

        if record.subject not in subjects:

            subjects[record.subject] = {
                "attended": 0,
                "total": 0
            }

        subjects[
            record.subject
        ]["total"] += 1

        if record.status == "Present":

            subjects[
                record.subject
            ]["attended"] += 1

    # -----------------------------------------------------
    # PERCENTAGE
    # -----------------------------------------------------

    for subject in subjects:

        attended = subjects[
            subject
        ]["attended"]

        total = subjects[
            subject
        ]["total"]

        if total > 0:

            subjects[
                subject
            ]["percentage"] = round(
                (attended / total) * 100,
                2
            )

        else:

            subjects[
                subject
            ]["percentage"] = 0

    return render_template(
        "attendance.html",
        student=student,
        attendance_records=attendance_records,
        subjects=subjects
    )


# =========================================================
# STUDENT RESULTS
# =========================================================


# =========================================================
# STUDENT TIMETABLE
# =========================================================

@app.route("/timetable")
def timetable():

    student_id = session.get(
        "student_id"
    )

    if not student_id:

        return redirect("/")

    student = db.session.get(
        Student,
        student_id
    )

    if student is None:

        session.clear()

        return redirect("/")

    return render_template(
        "timetable.html",
        student=student
    )


# =========================================================
# TEACHER LOGIN PAGE
# =========================================================

@app.route("/teacher-login")
def teacher_login():

    return render_template(
        "teacher_login.html"
    )


# =========================================================
# TEACHER LOGIN
# =========================================================

@app.route(
    "/teacher-login",
    methods=["POST"]
)
def do_teacher_login():

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    ).strip()

    teacher = Teacher.query.filter_by(
        username=username
    ).first()

    if teacher and teacher.password == password:

        session.clear()

        session["teacher_id"] = teacher.id

        return redirect(
            "/teacher-dashboard"
        )

    return "Invalid teacher username or password"


# =========================================================
# TEACHER DASHBOARD
# =========================================================

@app.route("/teacher-dashboard")
def teacher_dashboard():

    teacher_id = session.get(
        "teacher_id"
    )

    if not teacher_id:

        return redirect(
            "/teacher-login"
        )

    teacher = db.session.get(
        Teacher,
        teacher_id
    )

    if teacher is None:

        session.clear()

        return redirect(
            "/teacher-login"
        )

    students = Student.query.order_by(
        Student.roll_number
    ).all()

    return render_template(
        "teacher_dashboard.html",
        teacher=teacher,
        students=students
    )


# =========================================================
# TEACHER ATTENDANCE
# =========================================================

@app.route(
    "/teacher-attendance",
    methods=["GET", "POST"]
)
def teacher_attendance():

    teacher_id = session.get(
        "teacher_id"
    )

    if not teacher_id:

        return redirect(
            "/teacher-login"
        )

    teacher = db.session.get(
        Teacher,
        teacher_id
    )

    if teacher is None:

        session.clear()

        return redirect(
            "/teacher-login"
        )

    # =====================================================
    # SAVE ATTENDANCE
    # =====================================================

    if request.method == "POST":

        subject = request.form.get(
            "subject",
            ""
        ).strip()

        attendance_date = request.form.get(
            "attendance_date",
            ""
        ).strip()

        if not subject:

            return "Please enter the subject"

        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        if not attendance_date:

            attendance_date = date.today().strftime(
                "%d-%m-%Y"
            )

        else:

            try:

                attendance_date = datetime.strptime(
                    attendance_date,
                    "%Y-%m-%d"
                ).strftime(
                    "%d-%m-%Y"
                )

            except ValueError:

                return "Invalid date format"

        # -------------------------------------------------
        # STUDENTS
        # -------------------------------------------------

        students = Student.query.order_by(
            Student.roll_number
        ).all()

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        for student in students:

            checkbox = request.form.get(
                f"attendance_{student.id}"
            )

            if checkbox == "present":

                status = "Present"

            else:

                status = "Absent"

            existing = Attendance.query.filter_by(
                student_id=student.id,
                subject=subject,
                attendance_date=attendance_date
            ).first()

            if existing:

                existing.status = status
                existing.teacher_id = teacher.id

            else:

                record = Attendance(
                    student_id=student.id,
                    subject=subject,
                    attendance_date=attendance_date,
                    status=status,
                    teacher_id=teacher.id
                )

                db.session.add(record)

        db.session.commit()

        return redirect(
            "/teacher-attendance"
        )

    # =====================================================
    # DISPLAY STUDENTS
    # =====================================================

    students = Student.query.order_by(
        Student.roll_number
    ).all()

    # =====================================================
    # ATTENDANCE HISTORY
    # =====================================================

    attendance_history = Attendance.query.order_by(
        Attendance.id.desc()
    ).all()

    return render_template(
        "teacher_attendance.html",
        teacher=teacher,
        students=students,
        attendance_history=attendance_history
    )


# =========================================================
# ADMIN LOGIN PAGE
# =========================================================

@app.route("/admin-login")
def admin_login():

    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin-login",
    methods=["POST"]
)
def do_admin_login():

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    ).strip()

    admin = Admin.query.filter_by(
        username=username
    ).first()

    if admin and admin.password == password:

        session.clear()

        session["admin_id"] = admin.id

        return redirect(
            "/admin-dashboard"
        )

    return "Invalid admin username or password"


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin-dashboard")
def admin_dashboard():

    admin_id = session.get(
        "admin_id"
    )

    if not admin_id:

        return redirect(
            "/admin-login"
        )

    admin = db.session.get(
        Admin,
        admin_id
    )

    if admin is None:

        session.clear()

        return redirect(
            "/admin-login"
        )

    attendance_records = Attendance.query.order_by(
        Attendance.id.desc()
    ).all()

    students = Student.query.order_by(
        Student.roll_number
    ).all()

    teachers = Teacher.query.order_by(
        Teacher.id
    ).all()

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        attendance_records=attendance_records,
        students=students,
        teachers=teachers
    )


# =========================================================
# ADMIN EDIT ATTENDANCE
# =========================================================

@app.route(
    "/admin/edit-attendance/<int:attendance_id>",
    methods=["GET", "POST"]
)
def admin_edit_attendance(attendance_id):

    admin_id = session.get(
        "admin_id"
    )

    if not admin_id:

        return redirect(
            "/admin-login"
        )

    record = db.session.get(
        Attendance,
        attendance_id
    )

    if record is None:

        return "Attendance record not found"

    if request.method == "POST":

        status = request.form.get(
            "status",
            ""
        ).strip()

        if status not in [
            "Present",
            "Absent"
        ]:

            return "Invalid attendance status"

        record.status = status

        db.session.commit()

        return redirect(
            "/admin-dashboard"
        )

    return render_template(
        "admin_edit_attendance.html",
        record=record
    )


# =========================================================
# ADMIN DELETE ATTENDANCE
# =========================================================

@app.route(
    "/admin/delete-attendance/<int:attendance_id>",
    methods=["POST"]
)
def admin_delete_attendance(attendance_id):

    admin_id = session.get(
        "admin_id"
    )

    if not admin_id:

        return redirect(
            "/admin-login"
        )

    record = db.session.get(
        Attendance,
        attendance_id
    )

    if record:

        db.session.delete(record)

        db.session.commit()

    return redirect(
        "/admin-dashboard"
    )

# =========================================================
# RESULTS
# =========================================================

@app.route("/results")
def results():

    student_id = session.get("student_id")

    if not student_id:
        return redirect("/")

    student = db.session.get(
        Student,
        student_id
    )

    if student is None:
        session.clear()
        return redirect("/")

    marks = Marks.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "results.html",
        student=student,
        marks=marks
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return "College Portal is running successfully!"

#=================
#time table
#=======

# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
