from app import db


class User(db.Model):
    __tablename__ = 'User'
    email = db.Column(db.String(100), primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    schoolID = db.Column(db.String(15), nullable=False)
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


class School(db.Model):
    __tablename__ = 'School'
    ID = db.Column(db.String(15), primary_key=True)
    schoolName = db.Column(db.String(100), nullable=False)

    users = db.relationship('User')

    def __init__(self, ID, schoolName):
        self.ID = ID
        self.schoolName = schoolName


class Assignment(db.Model):
    __tablename__ = 'Assignment'
    AID = db.Column(db.String(15), primary_key=True)
    assignmentName = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(10), nullable=False)

    def __init__(self, AID, assignmentName, description, deadline):
        self.AID = AID
        self.assignmentName = assignmentName
        self.description = description
        self.deadline = deadline
