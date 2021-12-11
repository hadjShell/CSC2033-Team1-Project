from app import db
from flask_login import UserMixin

"""
These classes link the python application to the tables within the database, providing easier reading, writing and 
editing; rather than using pure SQL. Each class represents each table that is in the database: the User class 
represents the table 'User' within the database.
-------------------------------------------------------------------------------------------------------------------
Created by Harry Sayer
"""


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    email = db.Column(db.String(100), primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    schoolID = db.Column(db.String(15), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    UID = db.Column(db.String(36), nullable=False)

    # relationships to other tables
    engages = db.relationship('Engage')
    takes = db.relationship('Take')
    creates = db.relationship('Create')

    def __init__(self, email, role, password, schoolID, firstName, surname, UID):
        self.email = email
        self.role = role
        self.password = password
        self.schoolID = schoolID
        self.firstName = firstName
        self.surname = surname
        self.UID = UID


class School(db.Model):
    __tablename__ = 'School'
    ID = db.Column(db.String(15), primary_key=True)
    schoolName = db.Column(db.String(100), nullable=False)

    # relationships to other tables
    users = db.relationship('User')

    def __init__(self, ID, schoolName):
        self.ID = ID
        self.schoolName = schoolName


class Course(db.Model):
    __tablename__ = 'Course'
    CID = db.Column(db.String(15), primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)

    engages = db.relationship('Engage')

    def __init__(self, CID, courseName):
        self.CID = CID
        self.courseName = courseName


class Engage(db.Model):
    __tablename__ = 'Engage'
    email = db.Column(db.String(100), primary_key=True)
    CID = db.Column(db.String(15), primary_key=True)

    def __init__(self, email, CID):
        self.email = email
        self.CID = CID


class Assignment(db.Model):
    __tablename__ = 'Assignment'
    AID = db.Column(db.String(15), primary_key=True)
    assignmentName = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(10), nullable=False)

    # relationships to other tables
    takes = db.relationship('Take')
    creates = db.relationship('Create')

    def __init__(self, AID, assignmentName, description, deadline):
        self.AID = AID
        self.assignmentName = assignmentName
        self.description = description
        self.deadline = deadline


class Take(db.Model):
    __tablename__ = 'Take'
    email = db.Column(db.String(100), primary_key=True)
    AID = db.Column(db.String(15), primary_key=True)
    submitTime = db.Column(db.DateTime, nullable=False)
    grade = db.Column(db.Float, nullable=True)

    def __init__(self, email, AID, submitTime, grade):
        self.email = email
        self.AID = AID
        self.submitTime = submitTime
        self.grade = grade


class Create(db.Model):
    __tablename__ = 'Create'
    email = db.Column(db.String(100), primary_key=True)
    AID = db.Column(db.String(15), primary_key=True)
    CreateTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, AID, createTime):
        self.email = email
        self.AID = AID
        self.createTime = createTime