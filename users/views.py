from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import logging
from app import db
from models import User, School
from users.forms import LoginForm, RegisterForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstName=form.firstName.data,
                        surname=form.lastName.data,
                        password=form.password.data,
                        #                        pin_key=form.pin_key.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect((url_for('users.login')))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# Login page view
# Author: Jiayuan Zhang
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (form.password.data == user.password):

            # TODO: override get_id
            login_user(user)

            # Go to welcome page based on role
            if current_user.role == 'teacher':
                return redirect(url_for('users.welcome_teacher'))
            elif current_user.role == 'admin':
                return redirect(url_for('admins.admin'))
            else:
                # TODO: need to fix to student welcome page
                return redirect(url_for('users.welcome_teacher'))
        else:
            flash("Please check your login detail and try again!")

    return render_template('login.html', form=form)


# Teacher welcome view
# Author: Jiayuan Zhang
@users_blueprint.route('/welcome_teacher')
def welcome_teacher():
    return render_template('teacher-welcome.html', name=current_user.firstName)


# Profile view
# Author: Jiayuan Zhang
@users_blueprint.route('/profile')
def profile():
    return render_template('profile.html', firstName=current_user.firstName, surname=current_user.surname,
                           email=current_user.email, id=current_user.UID,
                           school=School.query.filter_by(ID=current_user.schoolID).first().schoolName)
