from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()