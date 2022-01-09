from app import db
from datetime import datetime
from flask_login import UserMixin

"""
These classes link the python application to the tables within the database, providing easier reading, writing and 
editing; rather than using pure SQL. Each class represents each table that is in the database: the User class 
represents the table 'User' within the database.
-------------------------------------------------------------------------------------------------------------------
Author: Jiayuan Zhang, Harry Sayer
"""


class School(db.Model):
    __tablename__ = 'School'
    ID = db.Column(db.Integer, primary_key=True)
    schoolName = db.Column(db.String(100), nullable=False)

    def __init__(self, schoolName):
        self.schoolName = schoolName


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    email = db.Column(db.String(100), primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    schoolID = db.Column(db.String(15), db.ForeignKey(School.ID), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    UID = db.Column(db.String(36), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, role, password, schoolID, firstName, surname, UID, approved):
        self.email = email
        self.role = role
        self.password = password
        self.schoolID = schoolID
        self.firstName = firstName
        self.surname = surname
        self.UID = UID
        self.approved = approved

    # override get_id
    def get_id(self):
        return self.email


class Course(db.Model):
    __tablename__ = 'Course'

    CID = db.Column(db.String(15), primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)

    def __init__(self, CID, courseName):
        self.CID = CID
        self.courseName = courseName


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

    def __init__(self, email, AID, submitTime, grade):
        self.email = email
        self.AID = AID
        self.submitTime = submitTime
        self.grade = grade


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

    school = School(schoolName="NCL UNI")

    test = User(email="test@email.com",
                password="password",
                role="teacher",
                schoolID="001",
                firstName="John",
                surname="Curry",
                UID="200511111",
                approved=True)
    test2 = User(email="test2@email.com",
                 password="password",
                 role="teacher",
                 schoolID="001",
                 firstName="Mark",
                 surname="Jones",
                 UID="200511122",
                 approved=True)
    test3 = User(email="test3@email.com",
                 password="password",
                 role="teacher",
                 schoolID="001",
                 firstName="Steve",
                 surname="Jobs",
                 UID="200511133",
                 approved=True)

    student1 = User(email="stu1@email.com",
                    password="password",
                    role="student",
                    schoolID="001",
                    firstName="Rob",
                    surname="S",
                    UID="000000001",
                    approved=True)
    student2 = User(email="stu2@email.com",
                    password="password",
                    role="student",
                    schoolID="001",
                    firstName="Jelly",
                    surname="S",
                    UID="000000002",
                    approved=True)
    student3 = User(email="stu3@email.com",
                    password="password",
                    role="student",
                    schoolID="001",
                    firstName="Bob",
                    surname="S",
                    UID="000000003",
                    approved=True)
    student4 = User(email="stu4@email.com",
                    password="password",
                    role="student",
                    schoolID="001",
                    firstName="Jack",
                    surname="S",
                    UID="000000004",
                    approved=True)

    course1 = Course(CID="CSC1031", courseName="Discrete Mathematics")
    course2 = Course(CID="CSC1032", courseName="Computer System")
    course3 = Course(CID="CSC1033", courseName="Database Management System")
    course4 = Course(CID="CSC1034", courseName="Python")
    course5 = Course(CID="CSC1035", courseName="Java")
    course6 = Course(CID="CSC2032", courseName="Algorithm Design and Analysis")

    assignment1 = Assignment(AID=1,
                             assignmentName="Programming",
                             description="This is a programming assignment for CSC1031.",
                             deadline=datetime(2022, 1, 1, 23, 59, 59),
                             CID="CSC1031",
                             doc_name='Programming.docx',
                             doc_path='/static/uploads/CSC1031/Programming.docx')
    assignment2 = Assignment(AID=2,
                             assignmentName="Report",
                             description="This is a report assignment for CSC1031.",
                             deadline=datetime(2021, 1, 1, 23, 59, 59),
                             CID="CSC1031",
                             doc_name='Report.docx',
                             doc_path='/static/uploads/CSC1031/Report.docx')
    assignment3 = Assignment(AID=3,
                             assignmentName="Essay",
                             description="This is an essay assignment for CSC1031.",
                             deadline=datetime(2021, 10, 1, 23, 59, 59),
                             CID="CSC1031",
                             doc_name='Essay.docx',
                             doc_path='/static/uploads/CSC1031/Essay.docx')

    engage1 = Engage(email="test@email.com", CID="CSC1031")
    engage2 = Engage(email="test@email.com", CID="CSC1032")
    engage3 = Engage(email="test@email.com", CID="CSC1033")
    engage4 = Engage(email="test@email.com", CID="CSC1034")
    engage5 = Engage(email="test2@email.com", CID="CSC1035")
    engage6 = Engage(email="stu1@email.com", CID="CSC1031")
    engage7 = Engage(email="stu2@email.com", CID="CSC1031")
    engage8 = Engage(email="stu3@email.com", CID="CSC1031")
    engage9 = Engage(email="stu4@email.com", CID="CSC1032")
    engage10 = Engage(email="test@email.com", CID="CSC2032")

    create1 = Create(email="test@email.com", AID=1)
    create2 = Create(email="test@email.com", AID=2)
    create3 = Create(email="test@email.com", AID=3)

    # be careful to the take object creation for test
    # students taking an assignment should be engaged in the related course first!!!
    # --- Jiayuan Zhang
    take1 = Take(email="stu1@email.com",
                 AID=2,
                 submitTime=datetime(2021, 1, 1, 22, 10, 10),
                 grade=92.3)
    take2 = Take(email="stu2@email.com",
                 AID=2,
                 submitTime=datetime(2021, 1, 1, 22, 48, 10),
                 grade=87.6)
    take3 = Take(email="stu3@email.com",
                 AID=2,
                 submitTime=None,
                 grade=None
                 )
    take4 = Take(email="stu1@email.com",
                 AID=1,
                 submitTime=None,
                 grade=None)

    db.session.add(school)
    db.session.add(test)
    db.session.add(test2)
    db.session.add(test3)
    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(student4)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    db.session.add(course5)
    db.session.add(course6)
    db.session.add(assignment1)
    db.session.add(assignment2)
    db.session.add(assignment3)
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
    db.session.add(create1)
    db.session.add(create2)
    db.session.add(create3)
    db.session.add(take1)
    db.session.add(take2)
    db.session.add(take3)
    db.session.add(take4)
    db.session.commit()
