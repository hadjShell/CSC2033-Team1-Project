# IMPORTS
from wtforms import StringField, SubmitField, SelectField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

"""
This python file contains all WTForms and restrictions related to admin activities.
-------------------------------------------------------------------------------------------------------------------
Created by Jiayuan Zhang
"""


# FORMS
class CreateSchoolForm(FlaskForm):
    schoolName = StringField(validators=[DataRequired()])
    submit = SubmitField()


class AddPeopleForm(FlaskForm):
    course_id = SelectField('Course ID', choices=[])
    email = StringField(validators=[DataRequired(), Email()])
    role = SelectField('role', choices=['teacher', 'student'])
    submit = SubmitField()


class UpdateCourseForm(FlaskForm):
    course_id = SelectField('Course ID', choices=[])
    new_course_name = StringField(validators=[DataRequired()])
    submit = SubmitField()


class DeleteCourseForm(FlaskForm):
    course_id = SelectField('Course ID', choices=[])
    submit = SubmitField()


class UpdateAssignmentForm(FlaskForm):
    assignment = SelectField('Assignment', choices=[])
    new_file = FileField(validators=[DataRequired()])
    submit = SubmitField()


class DeleteAssignmentForm(FlaskForm):
    assignment = SelectField('Assignment', choices=[])
    submit = SubmitField()


class ApproveForm(FlaskForm):
    email = SelectField('Unapproved', choices=[])
    decision = SelectField('Decision', choices=['Yes', 'No'])
    submit = SubmitField()
