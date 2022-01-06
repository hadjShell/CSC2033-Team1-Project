from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired
from models import User, Engage
from flask_login import current_user


def get_teacher_course():
    teacher_course_list = []
    course = Engage.query.filter_by(email=current_user.email).all()
    for c in course:
        teacher_course_list.append(Engage.query.filter_by(AID=c.AID).first())
    return teacher_course_list


# Form for creating an assignment
# Author: Tom Dawson
class AssignmentForm(FlaskForm):
    assignmentTitle = StringField('Assignment Title', validators=[DataRequired(message="Assignment must have title")])
    assignmentDescription = StringField('Assignment Description', validators=[DataRequired("Assignment must have "
                                                                                           "description")])
    assignmentDeadline = DateField('Assignment Deadline', validators=[DataRequired(message="Assignment must have a "
                                                                                           "deadline")],
                                   format='%d/%m/%Y')
    assignmentCID = SelectField('Course ID', choices=[get_teacher_course()], validators=DataRequired(message="Assignment must correspond to a course"))
    submit = SubmitField()
