# IMPORTS
from wtforms import StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class CreateSchoolForm(FlaskForm):
    schoolName = StringField(validators=[DataRequired()])
    submit = SubmitField()


class AddPeopleForm(FlaskForm):
    course_id = SelectField('Course ID', choices=[])
    email = StringField(validators=[DataRequired(), Email()])
    role = SelectField('role', choices=['teacher', 'student'])
    submit = SubmitField()
