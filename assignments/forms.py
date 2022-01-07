from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired
from models import User, Engage
from flask_login import current_user


# Form for creating an assignment
# Author: Tom Dawson
class AssignmentForm(FlaskForm):
    assignmentTitle = StringField('Assignment Title', validators=[DataRequired(message="Assignment must have title")])
    assignmentDescription = StringField('Assignment Description', validators=[DataRequired("Assignment must have "
                                                                                           "description")])
    assignmentDeadline = DateField('Assignment Deadline', validators=[DataRequired(message="Assignment must have a "
                                                                                           "deadline")],
                                   format='%d/%m/%Y')
    assignmentCID = SelectField('Course ID', validators=[DataRequired(message="Assignment must correspond to a course")])
    submit = SubmitField()
