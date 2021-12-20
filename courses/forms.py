from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):
    course_name = StringField(validators=[DataRequired(message="Course must have a name.")])
    submit = SubmitField()
