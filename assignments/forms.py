from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired


class AssignmentForm(FlaskForm):
    assignmentTitle = StringField(validators=[DataRequired(message="Assignment must have title")])
    assignmentDescription = StringField(validators=[DataRequired("Assignment must have description")])
    assignmentDeadline = DateField(validators=[DataRequired(message="Assignment must have a deadline")], format='%d/%m/%Y')
    assignmentCID = StringField(validators=[DataRequired(message="Assignment must correspond to a course")])
    submit = SubmitField()
