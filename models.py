from app import db


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
