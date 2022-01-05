from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class SelectStudents(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# Form for creating an assignment
# Author: Tom Dawson
class AssignmentForm(FlaskForm):
    assignmentTitle = StringField(validators=[DataRequired(message="Assignment must have title")])
    assignmentDescription = StringField(validators=[DataRequired("Assignment must have description")])
    assignmentDeadline = DateField(validators=[DataRequired(message="Assignment must have a deadline")],
                                   format='%d/%m/%Y')
    assignmentCID = StringField(validators=[DataRequired(message="Assignment must correspond to a course")])
    added_students = SelectStudents(u'Add students who will see the assignment')
    submit = SubmitField()
