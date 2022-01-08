# IMPORTS
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

"""
This python file contains all WTForms and restrictions related to course activities.
-------------------------------------------------------------------------------------------------------------------
Created by Jiayuan Zhang
"""


# HELP FUNCTIONS
# check if a course id is in format of 3 upper letters and 4 digits
def validate_course_id(form, field):
    p = re.compile(r'[A-Z]{3}[0-9]{4}')
    if not p.match(field.data):
        raise ValidationError(
            "Invalid Course ID!")


# FORMS
class CourseForm(FlaskForm):
    course_id = StringField(validators=[DataRequired(), validate_course_id])
    course_name = StringField(validators=[DataRequired()])
    submit = SubmitField()


class JoinForm(FlaskForm):
    course_id = StringField(validators=[DataRequired(), validate_course_id])
    submit = SubmitField()
