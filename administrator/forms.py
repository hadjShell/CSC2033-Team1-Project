# IMPORTS
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class CreateSchoolForm(FlaskForm):
    schoolName = StringField(validators=[DataRequired()])
    submit = SubmitField()


class CreateCourseForm(FlaskForm):
    CID = StringField(validators=[DataRequired()])
    courseName = StringField(validators=[DataRequired()])
    submit = SubmitField()
