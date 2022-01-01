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
    ID = db.Column(db.String(15), primary_key=True)
    schoolName = db.Column(db.String(100), nullable=False)

    def __init__(self, ID, schoolName):
        self.ID = ID
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

    def __init__(self, email, role, password, schoolID, firstName, surname, UID):
        self.email = email
        self.role = role
        self.password = password
        self.schoolID = schoolID
        self.firstName = firstName
        self.surname = surname
        self.UID = UID

    # override get_id
    def get_id(self):
        return self.email


class Course(db.Model):
    __tablename__ = 'Course'

    CID = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)

    def __init__(self, coursename):
        self.courseName = coursename


class Assignment(db.Model):
    __tablename__ = 'Assignment'

    AID = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey(User.email), nullable=False)
    assignmentName = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    CID = db.Column(db.Integer, db.ForeignKey(Course.CID), nullable=False)

    def __init__(self, email, assignmentName, description, deadline, CID):
        self.email = email
        self.assignmentName = assignmentName
        self.created = datetime.now()
        self.description = description
        self.deadline = deadline
        self.CID = CID


# Teachers engage in courses
class Engage(db.Model):
    __tablename__ = 'Engage'
    email = db.Column(db.String(100), db.ForeignKey(User.email), primary_key=True)
    CID = db.Column(db.Integer, db.ForeignKey(Course.CID), primary_key=True)

    def __init__(self, email, CID):
        self.email = email
        self.CID = CID


# Students take assignments
class Take(db.Model):
    __tablename__ = 'Take'

    email = db.Column(db.String(100), db.ForeignKey(User.email), primary_key=True)
    AID = db.Column(db.String(10), db.ForeignKey(Assignment.AID), primary_key=True)
    submitTime = db.Column(db.DateTime, nullable=False)
    grade = db.Column(db.Float, nullable=True)

    def __init__(self, email, AID, grade):
        self.email = email
        self.AID = AID
        self.submitTime = datetime.now()
        self.grade = grade


# Teachers create assignments
class Create(db.Model):
    __tablename__ = 'Create'

    email = db.Column(db.String(100), db.ForeignKey(User.email), primary_key=True)
    AID = db.Column(db.String(10), db.ForeignKey(Assignment.AID), primary_key=True)
    CreateTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, AID):
        self.email = email
        self.AID = AID
        self.createTime = datetime.now()


def init_db():
    db.drop_all()
    db.create_all()

    school = School(ID="001", schoolName="NCL UNI")

    test = User(email="test@email.com",
                password="password",
                role="teacher",
                schoolID="001",
                firstName="John",
                surname="Curry",
                UID="200511111")
    test2 = User(email="test2@email.com",
                 password="password",
                 role="teacher",
                 schoolID="001",
                 firstName="Mark",
                 surname="Jones",
                 UID="200511122")
    test3 = User(email="test3@email.com",
                 password="password",
                 role="teacher",
                 schoolID="001",
                 firstName="Steve",
                 surname="Jobs",
                 UID="200511122")

    course1 = Course(CID="CSC1031", courseName="Discrete Mathematics")
    course2 = Course(CID="CSC1032", courseName="Computer System")
    course3 = Course(CID="CSC1033", courseName="Database Management System")
    course4 = Course(CID="CSC1034", courseName="Python")
    course5 = Course(CID="CSC1035", courseName="Java")

    engage1 = Engage(email="test@email.com", CID="CSC1031")
    engage2 = Engage(email="test@email.com", CID="CSC1032")
    engage3 = Engage(email="test@email.com", CID="CSC1033")
    engage4 = Engage(email="test@email.com", CID="CSC1034")
    engage5 = Engage(email="test2@email.com", CID="CSC1035")

    db.session.add(school)
    db.session.add(test)
    db.session.add(test2)
    db.session.add(test3)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    db.session.add(course5)
    db.session.add(engage1)
    db.session.add(engage2)
    db.session.add(engage3)
    db.session.add(engage4)
    db.session.add(engage5)
    db.session.commit()
