from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TimeField, TextAreaField, FileField
from wtforms.validators import DataRequired
from app import db
from models import Course


def get_courses():
    return db.session.query(Course.CID).all()


# Form for creating an assignment
# Authors: Tom Dawson, Jiayuan Zhang
class AssignmentForm(FlaskForm):
    assignmentTitle = StringField('Assignment Title', validators=[DataRequired(message="Assignment must have title")])
    assignmentDescription = TextAreaField('Assignment Description', validators=[DataRequired("Assignment must have "
                                                                                           "description")])
    assignmentDeadlineDay = DateField('Assignment Deadline Day', validators=[DataRequired(message="Assignment must have a "
                                                                                           "deadline")])
    assignmentDeadlineTime = TimeField('Assignment Deadline Time', validators=[DataRequired(message="Assignment must "
                                                                                                    "have a "
                                                                                                    "deadline")])
    assignmentCID = SelectField('Course ID', choices=[])
    assignmentFile = FileField(validators=[DataRequired()])
    submit = SubmitField()


# Form for submitting answer
# Author: Jiayuan Zhang
class AnswerSubmissionForm(FlaskForm):
    assignment = SelectField('Assignment', choices=[])
    answerFile = FileField(validators=[DataRequired()])
    submit = SubmitField()
