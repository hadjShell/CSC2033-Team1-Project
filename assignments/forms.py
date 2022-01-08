from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from app import db
from models import Course


def get_courses():
    return db.session.query(Course.CID).all()


# Form for creating an assignment
# Author: Tom Dawson
class AssignmentForm(FlaskForm):
    assignmentTitle = StringField('Assignment Title', validators=[DataRequired(message="Assignment must have title")])
    assignmentDescription = StringField('Assignment Description', validators=[DataRequired("Assignment must have "
                                                                                           "description")])
    assignmentDeadline = DateField('Assignment Deadline', validators=[DataRequired(message="Assignment must have a "
                                                                                           "deadline")])
    assignmentCID = SelectField('Course ID', choices=[])
    submit = SubmitField()
