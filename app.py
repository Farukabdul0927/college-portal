from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime


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

    # Relationship with attendance
    attendance_records = db.relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # Relationship with marks
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

    # IMPORTANT:
    # This makes record.student work in HTML
    student = db.relationship(
        "Student",
        back_populates="attendance_records"
    )

    # This makes record.teacher work
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

students_data = [

    # =====================================================
    # CSE-A
    # =====================================================

    ("Y24CSE279001", "Abdul Sajida", "sajida001", "279001", "CSE-A"),
    ("Y24CSE279002", "Abu Taib", "taib002", "279002", "CSE-A"),
    ("Y24CSE279003", "Alluri Revakith Venkata Kumar", "kumar003", "279003", "CSE-A"),
    ("Y24CSE279004", "Aremanda Pujitha", "pujitha004", "279004", "CSE-A"),
    ("Y24CSE279005", "Atta Krishnam Naidu", "naidu005", "279005", "CSE-A"),
    ("Y24CSE279006", "Baipilli Gohini", "gohini006", "279006", "CSE-A"),
    ("Y24CSE279007", "Balagam Sri Lakshmi", "lakshmi007", "279007", "CSE-A"),
    ("Y24CSE279008", "Balagam Yohanu", "yohanu008", "279008", "CSE-A"),
    ("Y24CSE279009", "Balusupalli Anand Babu", "babu009", "279009", "CSE-A"),
    ("Y24CSE279010", "Basheerunisa", "basheerunisa010", "279010", "CSE-A"),
    ("Y24CSE279011", "Battula Gagan Chandra Moses", "moses011", "279011", "CSE-A"),
    ("Y24CSE279012", "Battula Ramu", "ramu012", "279012", "CSE-A"),
    ("Y24CSE279013", "Behara Gyaneswara Rao", "rao013", "279013", "CSE-A"),
    ("Y24CSE279014", "Bokinala Nikhil Babu", "babu014", "279014", "CSE-A"),
    ("Y24CSE279015", "Bon Kavya", "kavya015", "279015", "CSE-A"),
    ("Y24CSE279016", "Buraga Rohan Kumar", "kumar016", "279016", "CSE-A"),

    ("Y24CSE279018", "Chebathina Raghavendra", "raghavendra018", "279018", "CSE-A"),
    ("Y24CSE279019", "Chinnam Praneeth", "praneeth019", "279019", "CSE-A"),
    ("Y24CSE279020", "Chitajallu Vennela Sreya", "sreya020", "279020", "CSE-A"),
    ("Y24CSE279021", "Choragudi Sahith Babu", "babu021", "279021", "CSE-A"),
    ("Y24CSE279022", "Dalayi Devi Sri Deepa", "deepa022", "279022", "CSE-A"),
    ("Y24CSE279023", "Dandamudi Srivalli", "srivalli023", "279023", "CSE-A"),
    ("Y24CSE279024", "Dasari Naga Navya Sri", "sri024", "279024", "CSE-A"),
    ("Y24CSE279025", "Davu Nari Vardhani", "vardhani025", "279025", "CSE-A"),
    ("Y24CSE279026", "Deevi Syam Nikhil", "nikhil026", "279026", "CSE-A"),
    ("Y24CSE279027", "Deshik Badrachalam", "badrachalam027", "279027", "CSE-A"),
    ("Y24CSE279028", "Erikipati Akshaya", "akshaya028", "279028", "CSE-A"),
    ("Y24CSE279029", "Faruk Abdul", "abdul029", "279029", "CSE-A"),
    ("Y24CSE279030", "Gara Karthik", "karthik030", "279030", "CSE-A"),
    ("Y24CSE279031", "Gedala Naga Bhavani Anuradha", "anuradha031", "279031", "CSE-A"),
    ("Y24CSE279032", "Goli Venkata Padmavathi", "padmavathi032", "279032", "CSE-A"),
    ("Y24CSE279033", "Gosala Charishma", "charishma033", "279033", "CSE-A"),
    ("Y24CSE279034", "Gudapati Surendra", "surendra034", "279034", "CSE-A"),
    ("Y24CSE279035", "Gudaru Kalyani", "kalyani035", "279035", "CSE-A"),
    ("Y24CSE279036", "Irigi Harish", "harish036", "279036", "CSE-A"),
    ("Y24CSE279037", "Jakka Rama Venkata Aditya", "aditya037", "279037", "CSE-A"),

    ("Y24CSE279039", "Kalidindi Bhogesh", "bhogesh039", "279039", "CSE-A"),
    ("Y24CSE279040", "Kalyanapu Shyam Prasad", "prasad040", "279040", "CSE-A"),
    ("Y24CSE279041", "Kamapalli Mohammad Muniaf", "muniaf041", "279041", "CSE-A"),
    ("Y24CSE279042", "Kambhampati Madhu Babu", "babu042", "279042", "CSE-A"),
    ("Y24CSE279043", "Kanagala Naga Jayanthi", "jayanthi043", "279043", "CSE-A"),
    ("Y24CSE279044", "Kasi Lasya Sri Lalitha", "lalitha044", "279044", "CSE-A"),
    ("Y24CSE279045", "Katragadda Venkata Pavan Kumar", "kumar045", "279045", "CSE-A"),
    ("Y24CSE279046", "Katyala Lakshmanarao", "lakshmanarao046", "279046", "CSE-A"),
    ("Y24CSE279047", "Kayala Vyshnavi", "vyshnavi047", "279047", "CSE-A"),
    ("Y24CSE279048", "Kodeti Lakshmana Chandra", "chandra048", "279048", "CSE-A"),
    ("Y24CSE279049", "Kolikonda Tharun Kumar", "kumar049", "279049", "CSE-A"),
    ("Y24CSE279050", "Kommukuri Vardhan", "vardhan050", "279050", "CSE-A"),
    ("Y24CSE279051", "Kompalli Pavani Sai Sri", "sri051", "279051", "CSE-A"),
    ("Y24CSE279052", "Kondeti Neelima", "neelima052", "279052", "CSE-A"),
    ("Y24CSE279053", "Kondisetti Likitha", "likitha053", "279053", "CSE-A"),
    ("Y24CSE279054", "Konka Nikhil", "nikhil054", "279054", "CSE-A"),
    ("Y24CSE279055", "Kotnani Vinay", "vinay055", "279055", "CSE-A"),
    ("Y24CSE279056", "Kunchala Manoj Kumar", "kumar056", "279056", "CSE-A"),
    ("Y24CSE279057", "Likitha Kanchara", "kanchara057", "279057", "CSE-A"),
    ("Y24CSE279058", "Lokavarapu Hemalatha", "hemalatha058", "279058", "CSE-A"),
    ("Y24CSE279059", "Mahadevu Nageswararao", "nageswararao059", "279059", "CSE-A"),
    ("Y24CSE279060", "Manepalli Lokavinay Manikanta", "manikanta060", "279060", "CSE-A"),

    # =====================================================
    # CSE-B
    # =====================================================

    ("Y24CSE279061", "MANGALAPUDI MOHAN KUMAR", "kumar061", "279061", "CSE-B"),
    ("Y24CSE279062", "MARAPAKA SRESHA", "sresha062", "279062", "CSE-B"),
    ("Y24CSE279063", "MATHE VARDHAN", "vardhan063", "279063", "CSE-B"),
    ("Y24CSE279064", "MEESALA NITHIN", "nithin064", "279064", "CSE-B"),
    ("Y24CSE279065", "METTELA HARISH YADAV", "yadav065", "279065", "CSE-B"),
    ("Y24CSE279066", "MIRIYALA LOKESH", "lokesh066", "279066", "CSE-B"),
    ("Y24CSE279067", "MOTRU SASIKANTH", "sasikanth067", "279067", "CSE-B"),
    ("Y24CSE279068", "MUDAMANCHU RAJESH", "rajesh068", "279068", "CSE-B"),
    ("Y24CSE279069", "MUDUGU RAMYA", "ramya069", "279069", "CSE-B"),
    ("Y24CSE279070", "MUDUNURI ABHINAV", "abhinav070", "279070", "CSE-B"),
    ("Y24CSE279071", "MUNGANDA CHARAN KARTHIK", "karthik071", "279071", "CSE-B"),
    ("Y24CSE279072", "MUNIPALLI SIDDHARDA", "siddharda072", "279072", "CSE-B"),
    ("Y24CSE279073", "MURARI PREMANANDAM", "premanandam073", "279073", "CSE-B"),
    ("Y24CSE279074", "NAKKA PRAVEEN", "praveen074", "279074", "CSE-B"),

    ("Y24CSE279076", "NUTANGI SUBHASHINI", "subhashini076", "279076", "CSE-B"),
    ("Y24CSE279077", "PADAMATI SRI SAI DEEPAK RAJ", "raj077", "279077", "CSE-B"),
    ("Y24CSE279078", "PALAGANI RAMYA", "ramya078", "279078", "CSE-B"),
    ("Y24CSE279079", "PAMARTHI SAI SREE VENKATA SHANMUKHA", "shanmukha079", "279079", "CSE-B"),
    ("Y24CSE279080", "PANDIRI JAGADEESH", "jagadeesh080", "279080", "CSE-B"),
    ("Y24CSE279081", "PARAMESH NIRMALA DEVI NIKITHA", "nikitha081", "279081", "CSE-B"),
    ("Y24CSE279082", "PARASA ROHITH", "rohith082", "279082", "CSE-B"),
    ("Y24CSE279083", "PATIBANDLA CHIRISHMA", "chirishma083", "279083", "CSE-B"),
    ("Y24CSE279084", "PILLA CHARANMAI", "charanmai084", "279084", "CSE-B"),
    ("Y24CSE279085", "POLIPILLI PAWAN KUMAR", "kumar085", "279085", "CSE-B"),
    ("Y24CSE279086", "PONUGOTI STEEPHEN", "steephen086", "279086", "CSE-B"),

    ("Y24CSE279088", "PULI NAVYA SREE", "sree088", "279088", "CSE-B"),
    ("Y24CSE279089", "PULI YAMINI", "yamini089", "279089", "CSE-B"),
    ("Y24CSE279090", "RAMISETTI VENKATANADH", "venkatanadh090", "279090", "CSE-B"),
    ("Y24CSE279091", "RAVURI JYOTHI", "jyothi091", "279091", "CSE-B"),
    ("Y24CSE279092", "ROTHULA VENKATA KUMAR", "kumar092", "279092", "CSE-B"),
    ("Y24CSE279093", "SABA FATHEMA", "fathema093", "279093", "CSE-B"),
    ("Y24CSE279094", "SEELA VENKATA TEJA", "teja094", "279094", "CSE-B"),
    ("Y24CSE279095", "SHAIK ABBAS VALI", "vali095", "279095", "CSE-B"),
    ("Y24CSE279096", "SHAIK ABDULLA", "abdulla096", "279096", "CSE-B"),
    ("Y24CSE279097", "SHAIK NAGULMEERA", "nagulmeera097", "279097", "CSE-B"),
    ("Y24CSE279098", "SURISETTI RAMAKRISHNA", "ramakrishna098", "279098", "CSE-B"),
    ("Y24CSE279099", "SYED GULAME RASOOL", "rasool099", "279099", "CSE-B"),
    ("Y24CSE279100", "SYKAM BHAVYA", "bhavya100", "279100", "CSE-B"),
    ("Y24CSE279101", "THAMMU MANI SANKAR VENKATA GANESH", "ganesh101", "279101", "CSE-B"),
    ("Y24CSE279102", "THIPPANA SANTHOSH", "santhosh102", "279102", "CSE-B"),
    ("Y24CSE279103", "THOKALA SAIDULU RAJU", "raju103", "279103", "CSE-B"),
    ("Y24CSE279104", "TIKKISETTY RAMYA SREE LAKSHMI", "lakshmi104", "279104", "CSE-B"),
    ("Y24CSE279105", "UNDAPALLI KEERTHI", "keerthi105", "279105", "CSE-B"),
    ("Y24CSE279106", "VAYYAVURU BHAVANA", "bhavana106", "279106", "CSE-B"),
    ("Y24CSE279107", "VEMU VAMSI KUMAR", "kumar107", "279107", "CSE-B"),
    ("Y24CSE279108", "YANNA SRINIVAS", "srinivas108", "279108", "CSE-B"),
    ("Y24CSE279109", "YARAGORLA GOPI", "gopi109", "279109", "CSE-B"),
]


# =========================================================
# ORIGINAL TEACHER DATA
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

ORIGINAL_ATTENDANCE = {

    "29-07-2026": {
        "A": [2, 29],
        "B": [68, 79, 95, 105]
    },

    "31-07-2026": {
        "A": [48],
        "B": [68, 73, 77, 79, 93, 95, 101, 104, 105, 110]
    },

    "04-08-2026": {
        "A": [
            3, 7, 14, 15, 18, 20, 21, 22,
            24, 28, 31, 32, 35, 43, 45, 47,
            48, 53, 57
        ],
        "B": [
            64, 68, 70, 71, 72, 73, 76, 77,
            78, 79, 84, 88, 93, 95, 99, 100,
            101, 104, 105, 108, 110
        ]
    },

    "06-08-2026": {
        "A": [
            2, 5, 6, 7, 14, 15, 18, 20,
            21, 23, 24, 25, 28, 29, 30, 31,
            32, 35, 40, 42, 43, 45, 48, 57, 58
        ],
        "B": [
            64, 67, 68, 70, 71, 72, 73, 76,
            77, 78, 79, 84, 88, 89, 91, 93,
            95, 99, 100, 103, 105, 108
        ]
    },

    "07-08-2026": {
        "A": [
            1, 2, 5, 7, 10, 14, 15, 18,
            20, 21, 22, 24, 29, 31, 35, 40,
            43, 45, 47, 48, 53, 58
        ],
        "B": [
            67, 68, 71, 73, 77, 78, 88, 89,
            93, 95, 100, 101, 104, 105, 108, 110
        ]
    },

    "10-08-2026": {
        "A": [
            1, 2, 3, 5, 6, 7, 8, 10,
            12, 14, 15, 18, 20, 21, 22, 23,
            24, 28, 29, 30, 31, 32, 33, 35,
            40, 43, 44, 45, 47, 48, 51, 52,
            53, 57, 58
        ],
        "B": [
            64, 66, 67, 68, 71, 72, 73, 76,
            77, 78, 79, 81, 84, 85, 88, 89,
            90, 92, 93, 95, 99, 100, 101, 103,
            104, 105, 107, 108, 110
        ]
    },

    "11-08-2026": {
        "A": [
            1, 2, 5, 6, 7, 8, 10, 12,
            14, 15, 18, 20, 21, 22, 23, 24,
            26, 28, 29, 30, 31, 32, 33, 35,
            40, 42, 43, 44, 51, 52, 53, 55,
            57, 58
        ],
        "B": [
            64, 65, 67, 68, 70, 71, 72, 73,
            74, 76, 77, 78, 79, 81, 84, 88,
            89, 90, 92, 93, 95, 99, 100, 101,
            103, 104, 105, 107, 108, 109, 110
        ]
    },

    "12-08-2026": {
        "A": [
            1, 2, 5, 8, 10, 12, 14, 20,
            21, 22, 23, 24, 29, 30, 31, 32,
            33, 40, 42, 44, 45, 47, 48, 51,
            52, 53, 55, 57, 58
        ],
        "B": [
            65, 67, 68, 70, 71, 72, 73, 76,
            77, 78, 79, 81, 84, 88, 89, 90,
            95, 99, 100, 103, 104, 105, 106,
            107, 108, 109, 110
        ]
    },

    "13-08-2026": {
        "A": [
            1, 2, 5, 6, 7, 10, 12, 15,
            18, 20, 21, 22, 23, 24, 29, 30,
            31, 32, 33, 41, 42, 43, 44, 46,
            47, 48, 49, 52, 53, 55, 58
        ],
        "B": [
            64, 65, 67, 68, 71, 72, 73, 76,
            77, 78, 79, 81, 84, 85, 86, 88,
            90, 91, 93, 95, 100, 104, 105, 108,
            109
        ]
    },

    "14-08-2026": {
        "A": [
            1, 2, 5, 6, 7, 8, 9, 10,
            12, 14, 20, 21, 22, 24, 26, 29,
            30, 31, 32, 33, 39, 40, 41, 43,
            44, 45, 47, 48, 51, 52, 53, 55,
            57, 58
        ],
        "B": [
            64, 67, 68, 70, 71, 72, 73, 76,
            77, 78, 79, 84, 88, 89, 90, 93,
            95, 100, 105, 106, 107, 108
        ]
    },

    "17-08-2026": {
        "A": [
            1, 2, 3, 7, 10, 12, 14, 15,
            16, 18, 20, 21, 22, 23, 24, 26,
            30, 31, 32, 33, 40, 41, 42, 45,
            46, 47, 48, 49, 51, 52, 53, 55,
            57, 58
        ],
        "B": [
            62, 67, 68, 70, 71, 72, 73, 76,
            77, 78, 79, 80, 84, 86, 88, 89,
            90, 92, 93, 95, 99, 100, 105, 106,
            107, 108, 109, 110
        ]
    },

    "18-08-2026": {
        "A": [
            2, 6, 7, 12, 14, 15, 16, 18,
            19, 20, 21, 22, 23, 24, 26, 29,
            31, 32, 33, 36, 39, 40, 41, 42,
            44, 45, 47, 51, 52, 53, 55, 57
        ],
        "B": [
            62, 64, 67, 68, 70, 72, 73, 77,
            80, 84, 86, 88, 89, 90, 92, 93,
            95, 99, 100, 105, 106, 107, 110
        ]
    },

    "19-08-2026": {
        "A": [
            1, 2, 5, 6, 7, 9, 10, 14,
            16, 20, 21, 24, 29, 30, 31, 32,
            35, 40, 42, 43, 44, 45, 47, 48,
            52, 53, 57, 58
        ],
        "B": [
            62, 64, 67, 68, 70, 71, 72, 73,
            77, 78, 79, 80, 85, 86, 88, 90,
            91, 93, 94, 95, 99, 100, 104, 106,
            108
        ]
    },

    "20-08-2026": {
        "A": [
            1, 2, 3, 6, 7, 10, 12, 15,
            18, 20, 21, 22, 24, 29, 31, 32,
            33, 34, 35, 40, 41, 43, 44, 45,
            46, 47, 48, 51, 53, 57, 58
        ],
        "B": [
            62, 64, 67, 71, 72, 73, 76, 77,
            79, 84, 88, 89, 90, 91, 92, 93,
            94, 95, 99, 100, 101, 103, 104, 105,
            106, 108, 109
        ]
    },

    "22-08-2026": {
        "A": [
            12, 14, 19, 21, 24, 28, 31, 32,
            33, 40, 41, 45, 47, 48, 52, 57
        ],
        "B": [
            62, 64, 67, 68, 71, 73, 76, 77,
            78, 79, 84, 88, 91, 93, 95, 100,
            105, 106
        ]
    },

    "24-08-2026": {
        "A": [
            1, 2, 4, 5, 7, 8, 9, 10,
            14, 15, 18, 20, 21, 22, 24, 26,
            30, 32, 33, 34, 35, 36, 41, 42,
            43, 45, 47, 48, 50, 51, 53, 57
        ],
        "B": [
            62, 64, 68, 70, 71, 72, 73, 74,
            77, 78, 79, 84, 88, 89, 90, 91,
            93, 95, 96, 97, 100, 103, 104, 105,
            106, 107, 109, 110
        ]
    },

    "25-08-2026": {
        "A": [
            2, 4, 7, 8, 9, 12, 14, 16,
            20, 21, 22, 24, 26, 27, 29, 30,
            33, 35, 36, 40, 41, 42, 45, 46,
            47, 48, 49, 51, 53, 57
        ],
        "B": [
            61, 62, 64, 66, 67, 68, 70, 71,
            72, 73, 77, 78, 80, 81, 84, 85,
            88, 92, 93, 95, 99, 100, 101, 103,
            106, 107, 108, 110, 74, 94
        ]
    },

    "27-08-2026": {
        "A": [
            2, 4, 5, 6, 8, 14, 16, 20,
            21, 22, 24, 29, 30, 36, 41, 42,
            44, 47, 48, 49, 45, 51, 58, 53, 57
        ],
        "B": [
            61, 67, 77, 80, 88, 90, 93, 95,
            105, 106, 109, 110
        ]
    }
}


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    db.create_all()

    # =====================================================
    # CREATE / UPDATE 13 ORIGINAL TEACHERS
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
                except (ValueError, TypeError):
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
# LOGIN PAGE
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

    # =====================================================
    # GET ATTENDANCE
    # =====================================================

    attendance_records = Attendance.query.filter_by(
        student_id=student.id
    ).all()

    # =====================================================
    # FIX OLD DATE FORMAT
    # =====================================================

    changed = False

    for record in attendance_records:

        if record.attendance_date == "2026-08-27":

            record.attendance_date = "27-08-2026"

            changed = True

    if changed:

        db.session.commit()

    # =====================================================
    # SORT
    # =====================================================

    def sort_date(record):

        try:

            return datetime.strptime(
                record.attendance_date,
                "%d-%m-%Y"
            )

        except (ValueError, TypeError):

            return datetime.min

    attendance_records.sort(
        key=sort_date
    )

    # =====================================================
    # SUBJECT-WISE ATTENDANCE
    # =====================================================

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

    # =====================================================
    # PERCENTAGE
    # =====================================================

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

    # =====================================================
    # DISPLAY
    # =====================================================

    return render_template(
        "attendance.html",
        student=student,
        attendance_records=attendance_records,
        subjects=subjects
    )


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
        # GET STUDENTS
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

    # =====================================================
    # DISPLAY
    # =====================================================

    return render_template(
        "teacher_attendance.html",
        teacher=teacher,
        students=students,
        attendance_history=attendance_history
    )


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
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )