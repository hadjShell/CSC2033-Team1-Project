# IMPORTS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TimeField, TextAreaField, FileField
from wtforms.validators import DataRequired

"""
This python file contains all WTForms and restrictions related to assignment activities.
-------------------------------------------------------------------------------------------------------------------
Created by Jiayuan Zhang, Tom Dawson
"""


# Form for creating an assignment
# Authors: Tom Dawson, Jiayuan Zhang
class AssignmentForm(FlaskForm):
    assignmentTitle = StringField('Assignment Title', validators=[DataRequired()])
    assignmentDescription = TextAreaField('Assignment Description', validators=[DataRequired()])
    assignmentDeadlineDay = DateField('Assignment Deadline Day', validators=[DataRequired()])
    assignmentDeadlineTime = TimeField('Assignment Deadline Time', validators=[DataRequired()])
    assignmentCID = SelectField('Course ID', choices=[])
    assignmentFile = FileField(validators=[DataRequired()])
    submit = SubmitField()


# Form for submitting answer
# Author: Jiayuan Zhang
class AnswerSubmissionForm(FlaskForm):
    assignment = SelectField('Assignment', choices=[])
    answerFile = FileField(validators=[DataRequired()])
    submit = SubmitField()
