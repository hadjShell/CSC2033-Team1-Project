from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class SelectStudents(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CourseForm(FlaskForm):
    course_name = StringField(validators=[DataRequired(message="Course must have a name.")])
    added_students = SelectStudents(u'Add users to your course')
    submit = SubmitField()