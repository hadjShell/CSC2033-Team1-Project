# IMPORTS
from app import db, ROOT_DIR
from pathlib import Path
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

"""
These classes link the python application to the tables within the database, providing easier reading, writing and 
editing; rather than using pure SQL. Each class represents each table that is in the database: the User class 
represents the table 'User' within the database.
-------------------------------------------------------------------------------------------------------------------
Author: Jiayuan Zhang, Harry Sayer
"""


# School table
class School(db.Model):
    __tablename__ = 'School'
    ID = db.Column(db.Integer, primary_key=True)
    schoolName = db.Column(db.String(100), nullable=False)

    def __init__(self, schoolName):
        self.schoolName = schoolName


# User table, contains teachers, students, admins
class User(db.Model, UserMixin):
    __tablename__ = 'User'

    email = db.Column(db.String(100), primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    schoolID = db.Column(db.Integer, db.ForeignKey(School.ID), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    UID = db.Column(db.String(36), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, role, password, schoolID, firstName, surname, UID, approved):
        self.email = email
        self.role = role
        self.password = generate_password_hash(password)
        self.schoolID = schoolID
        self.firstName = firstName
        self.surname = surname
        self.UID = UID
        self.approved = approved

    # override get_id
    def get_id(self):
        return self.email


# Course table
class Course(db.Model):
    __tablename__ = 'Course'

    CID = db.Column(db.String(15), primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)

    def __init__(self, CID, courseName):
        self.CID = CID
        self.courseName = courseName


# Assignment table
class Assignment(db.Model):
    __tablename__ = 'Assignment'

    AID = db.Column(db.Integer, primary_key=True)
    assignmentName = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    doc_name = db.Column(db.String(50), nullable=False)
    doc_path = db.Column(db.String(200), nullable=False)
    CID = db.Column(db.String(15), db.ForeignKey(Course.CID), nullable=False)

    def __init__(self, AID, assignmentName, description, deadline, doc_name, doc_path, CID):
        self.AID = AID
        self.assignmentName = assignmentName
        self.description = description
        self.deadline = deadline
        self.doc_name = doc_name
        self.doc_path = doc_path
        self.CID = CID


# Teachers and students engage in courses
class Engage(db.Model):
    __tablename__ = 'Engage'
    email = db.Column(db.String(100), db.ForeignKey(User.email), primary_key=True)
    CID = db.Column(db.String(15), db.ForeignKey(Course.CID), primary_key=True)

    def __init__(self, email, CID):
        self.email = email
        self.CID = CID


# Students take assignments
class Take(db.Model):
    __tablename__ = 'Take'

    email = db.Column(db.String(100), db.ForeignKey(User.email), primary_key=True)
    AID = db.Column(db.Integer, db.ForeignKey(Assignment.AID), primary_key=True)
    submitTime = db.Column(db.DateTime, nullable=True)
    grade = db.Column(db.Float, nullable=True)
    doc_name = db.Column(db.String(50), nullable=True)
    doc_path = db.Column(db.String(200), nullable=True)

    def __init__(self, email, AID, submitTime, grade):
        self.email = email
        self.AID = AID
        self.submitTime = submitTime
        self.grade = grade
        self.doc_name = None
        self.doc_path = None


# Teachers create assignments
class Create(db.Model):
    __tablename__ = 'Create'

    email = db.Column(db.String(100), db.ForeignKey(User.email), primary_key=True)
    AID = db.Column(db.Integer, db.ForeignKey(Assignment.AID), primary_key=True)
    createTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, AID):
        self.email = email
        self.AID = AID
        self.createTime = datetime.now()


def init_db():
    db.drop_all()
    db.create_all()

    school1 = School(schoolName="Newcastle University")
    school2 = School(schoolName="University of Cambridge")

    admin = User(email="admin@email.com",
                 password="Admin1!",
                 role="admin",
                 schoolID=1,
                 firstName="admin",
                 surname="admin",
                 UID="88888888",
                 approved=True
                 )

    test = User(email="test@email.com",
                password="Teacher1!",
                role="teacher",
                schoolID=1,
                firstName="John",
                surname="Curry",
                UID="20051111",
                approved=True)
    test2 = User(email="test2@email.com",
                 password="Teacher2!",
                 role="teacher",
                 schoolID=1,
                 firstName="Mark",
                 surname="Jones",
                 UID="20051112",
                 approved=True)
    test3 = User(email="test3@email.com",
                 password="Teacher3!",
                 role="teacher",
                 schoolID=2,
                 firstName="Steve",
                 surname="Jobs",
                 UID="20061111",
                 approved=True)

    student1 = User(email="stu1@email.com",
                    password="Student1!",
                    role="student",
                    schoolID=1,
                    firstName="Jiayuan",
                    surname="Zhang",
                    UID="10000001",
                    approved=True)
    # create submission folder
    path = ROOT_DIR / Path("static/students_submission/stu1@email.com")
    path.mkdir(parents=True, exist_ok=True)
    student2 = User(email="stu2@email.com",
                    password="Student2!",
                    role="student",
                    schoolID=1,
                    firstName="Jelly",
                    surname="Fisher",
                    UID="10000002",
                    approved=True)
    # create submission folder
    path = ROOT_DIR / Path("static/students_submission/stu2@email.com")
    path.mkdir(parents=True, exist_ok=True)
    student3 = User(email="stu3@email.com",
                    password="Student3!",
                    role="student",
                    schoolID=1,
                    firstName="Bob",
                    surname="Duncan",
                    UID="10000003",
                    approved=True)
    # create submission folder
    path = ROOT_DIR / Path("static/students_submission/stu3@email.com")
    path.mkdir(parents=True, exist_ok=True)
    student4 = User(email="stu4@email.com",
                    password="Student4!",
                    role="student",
                    schoolID=1,
                    firstName="Jack",
                    surname="Scott",
                    UID="10000004",
                    approved=True)
    # create submission folder
    path = ROOT_DIR / Path("static/students_submission/stu4@email.com")
    path.mkdir(parents=True, exist_ok=True)
    student5 = User(email="stu5@email.com",
                    password="Student5!",
                    role="student",
                    schoolID=2,
                    firstName="Emma",
                    surname="Quinn",
                    UID="20000001",
                    approved=True)
    # create submission folder
    path = ROOT_DIR / Path("static/students_submission/stu5@email.com")
    path.mkdir(parents=True, exist_ok=True)

    course1 = Course(CID="CSC1031", courseName="Discrete Mathematics")
    # create folder
    path = ROOT_DIR / Path("static/teachers_submission/CSC1031")
    path.mkdir(parents=True, exist_ok=True)
    course2 = Course(CID="CSC1032", courseName="Computer System")
    # create folder
    path = ROOT_DIR / Path("static/teachers_submission/CSC1032")
    path.mkdir(parents=True, exist_ok=True)
    course3 = Course(CID="CSC1033", courseName="Database Management System")
    # create folder
    path = ROOT_DIR / Path("static/teachers_submission/CSC1033")
    path.mkdir(parents=True, exist_ok=True)
    course4 = Course(CID="CSC1034", courseName="Python")
    # create folder
    path = ROOT_DIR / Path("static/teachers_submission/CSC1034")
    path.mkdir(parents=True, exist_ok=True)
    course5 = Course(CID="CSC1035", courseName="Java")
    # create folder
    path = ROOT_DIR / Path("static/teachers_submission/CSC1035")
    path.mkdir(parents=True, exist_ok=True)
    course6 = Course(CID="CSC2032", courseName="Algorithm Design and Analysis")
    # create folder
    path = ROOT_DIR / Path("static/teachers_submission/CSC2032")
    path.mkdir(parents=True, exist_ok=True)

    assignment1 = Assignment(AID=1,
                             assignmentName="Programming",
                             description="This is a programming assignment for CSC1031.",
                             deadline=datetime(2022, 1, 1, 23, 59, 59),
                             CID="CSC1031",
                             doc_name='Programming.docx',
                             doc_path='static/teachers_submission/CSC1031/Programming.docx')
    assignment2 = Assignment(AID=2,
                             assignmentName="Report",
                             description="This is a report assignment for CSC1031.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC1031",
                             doc_name='Report.docx',
                             doc_path='static/teachers_submission/CSC1031/Report.docx')
    assignment3 = Assignment(AID=3,
                             assignmentName="Essay",
                             description="This is an essay assignment for CSC1031.",
                             deadline=datetime(2021, 10, 1, 23, 59, 59),
                             CID="CSC1031",
                             doc_name='Essay.docx',
                             doc_path='static/teachers_submission/CSC1031/Essay.docx')
    assignment4 = Assignment(AID=4,
                             assignmentName="Coding",
                             description="This is a coding assignment for CSC1032.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC1032",
                             doc_name='Coding.docx',
                             doc_path='static/teachers_submission/CSC1032/Coding.docx')
    assignment5 = Assignment(AID=5,
                             assignmentName="Report",
                             description="This is a report assignment for CSC1033.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC1033",
                             doc_name='Report.docx',
                             doc_path='static/teachers_submission/CSC1033/Report.docx')
    assignment6 = Assignment(AID=6,
                             assignmentName="Report",
                             description="This is a report assignment for CSC1034.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC1034",
                             doc_name='Report.docx',
                             doc_path='static/teachers_submission/CSC1034/Report.docx')
    assignment7 = Assignment(AID=7,
                             assignmentName="Report",
                             description="This is a report assignment for CSC1035.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC1035",
                             doc_name='Report.docx',
                             doc_path='static/teachers_submission/CSC1035/Report.docx')
    assignment8 = Assignment(AID=8,
                             assignmentName="Report",
                             description="This is a report assignment for CSC2032.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC2032",
                             doc_name='Report.docx',
                             doc_path='static/teachers_submission/CSC2032/Report.docx')

    engage1 = Engage(email="test@email.com", CID="CSC1031")
    engage2 = Engage(email="test@email.com", CID="CSC1032")
    engage3 = Engage(email="test@email.com", CID="CSC1033")
    engage4 = Engage(email="test@email.com", CID="CSC1034")
    engage5 = Engage(email="test@email.com", CID="CSC1035")
    engage6 = Engage(email="test2@email.com", CID="CSC1035")
    engage7 = Engage(email="test3@email.com", CID="CSC2032")
    engage8 = Engage(email="stu1@email.com", CID="CSC1031")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu1@email.com/CSC1031")
    path.mkdir(parents=True, exist_ok=True)

    engage9 = Engage(email="stu1@email.com", CID="CSC1032")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu1@email.com/CSC1032")
    path.mkdir(parents=True, exist_ok=True)

    engage10 = Engage(email="stu1@email.com", CID="CSC1033")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu1@email.com/CSC1033")
    path.mkdir(parents=True, exist_ok=True)

    engage11 = Engage(email="stu1@email.com", CID="CSC1034")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu1@email.com/CSC1034")
    path.mkdir(parents=True, exist_ok=True)

    engage12 = Engage(email="stu2@email.com", CID="CSC1033")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu2@email.com/CSC1033")
    path.mkdir(parents=True, exist_ok=True)

    engage13 = Engage(email="stu3@email.com", CID="CSC1033")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu3@email.com/CSC1033")
    path.mkdir(parents=True, exist_ok=True)

    engage14 = Engage(email="stu4@email.com", CID="CSC1032")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu4@email.com/CSC1032")
    path.mkdir(parents=True, exist_ok=True)

    engage15 = Engage(email="stu5@email.com", CID="CSC2032")
    # create folder
    path = ROOT_DIR / Path("static/students_submission/stu5@email.com/CSC2032")
    path.mkdir(parents=True, exist_ok=True)

    create1 = Create(email="test@email.com", AID=1)
    create2 = Create(email="test@email.com", AID=2)
    create3 = Create(email="test@email.com", AID=3)
    create4 = Create(email="test@email.com", AID=4)
    create5 = Create(email="test@email.com", AID=5)
    create6 = Create(email="test@email.com", AID=6)
    create7 = Create(email="test@email.com", AID=7)
    create8 = Create(email="test2@email.com", AID=7)
    create9 = Create(email="test3@email.com", AID=8)

    # be careful to the take object creation for test
    # students taking an assignment should be engaged in the related course first!!!
    # --- Jiayuan Zhang
    take1 = Take(email="stu1@email.com",
                 AID=1,
                 submitTime=None,
                 grade=None)
    take2 = Take(email="stu1@email.com",
                 AID=2,
                 submitTime=None,
                 grade=None)
    take3 = Take(email="stu1@email.com",
                 AID=3,
                 submitTime=None,
                 grade=None
                 )
    take4 = Take(email="stu1@email.com",
                 AID=4,
                 submitTime=None,
                 grade=None)
    take5 = Take(email="stu1@email.com",
                 AID=5,
                 submitTime=None,
                 grade=None)
    take6 = Take(email="stu1@email.com",
                 AID=6,
                 submitTime=None,
                 grade=None)
    take7 = Take(email="stu2@email.com",
                 AID=5,
                 submitTime=None,
                 grade=None)
    take8 = Take(email="stu3@email.com",
                 AID=5,
                 submitTime=None,
                 grade=None)
    take9 = Take(email="stu4@email.com",
                  AID=4,
                  submitTime=None,
                  grade=None)
    take10 = Take(email="stu5@email.com",
                  AID=8,
                  submitTime=None,
                  grade=None)

    db.session.add(school1)
    db.session.add(school2)
    db.session.add(admin)
    db.session.add(test)
    db.session.add(test2)
    db.session.add(test3)
    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(student4)
    db.session.add(student5)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    db.session.add(course5)
    db.session.add(course6)
    db.session.add(assignment1)
    db.session.add(assignment2)
    db.session.add(assignment3)
    db.session.add(assignment4)
    db.session.add(assignment5)
    db.session.add(assignment6)
    db.session.add(assignment7)
    db.session.add(assignment8)
    db.session.add(engage1)
    db.session.add(engage2)
    db.session.add(engage3)
    db.session.add(engage4)
    db.session.add(engage5)
    db.session.add(engage6)
    db.session.add(engage7)
    db.session.add(engage8)
    db.session.add(engage9)
    db.session.add(engage10)
    db.session.add(engage11)
    db.session.add(engage12)
    db.session.add(engage13)
    db.session.add(engage14)
    db.session.add(engage15)
    db.session.add(create1)
    db.session.add(create2)
    db.session.add(create3)
    db.session.add(create4)
    db.session.add(create5)
    db.session.add(create6)
    db.session.add(create7)
    db.session.add(create8)
    db.session.add(create9)
    db.session.add(take1)
    db.session.add(take2)
    db.session.add(take3)
    db.session.add(take4)
    db.session.add(take5)
    db.session.add(take6)
    db.session.add(take7)
    db.session.add(take8)
    db.session.add(take9)
    db.session.add(take10)
    db.session.commit()
