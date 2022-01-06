import re
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


# All registration forms must be filled (via Required import) & email must be a valid email layout


# check if a field contains specific characters and digits, return error if yes
def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>0123456789"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    firstName = StringField(validators=[DataRequired(), character_check])
    lastName = StringField(validators=[DataRequired(), character_check])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message='Password must be between 6 '
                                                                                       'and 12 characters in length.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal!')])
    # School name/id to do
    #    pin_key = StringField(validators=[DataRequired(), Length(min=32, max=32, message='Pin key must be exactly 32 '
    #                                                                                 'characters in length')])
    submit = SubmitField()

    # check if password contains at least 1 digit, 1 lowercase, 1 uppercase and 1 special character, return error if not
    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])')
        if not p.match(self.password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special character.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12,
                                                                    message='Password must be between 6 '
                                                                            'and 12 characters in length.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='Both password fields '
                                                                                             'must be equal!')])
    submit = SubmitField()

    # check if new password contains at least 1 digit, 1 lowercase, 1 uppercase and 1 special character,
    # return error if not
    def validate_password(self, new_password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])')
        if not p.match(self.new_password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special character.")
