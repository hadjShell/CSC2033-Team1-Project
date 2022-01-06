# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
import logging
from app import db, login_required, requires_roles
from models import User, School, Take, Assignment
from users.forms import LoginForm, RegisterForm, ChangePasswordForm

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
# Authors: Uzair Yousaf, Harry Sayer
@users_blueprint.route('/register', methods=['GET', 'POST'])
@requires_roles()
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

        logging.warning('SECURITY - USER REGISTRATION|%s|%s|%s', new_user.UID, new_user.email,
                        request.remote_addr)

        # sends user to login page
        return redirect((url_for('users.login')))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# Login page view
# Authors: Jiayuan Zhang, Harry Sayer
@users_blueprint.route('/login', methods=['GET', 'POST'])
@requires_roles()
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (form.password.data == user.password):
            login_user(user)

            logging.warning('SECURITY - USER LOG IN|%s|%s|%s', current_user.UID, current_user.email,
                            request.remote_addr)

            # Go to welcome page based on role
            if current_user.role == 'teacher':
                return redirect(url_for('users.welcome_teacher'))
            elif current_user.role == 'admin':
                return redirect(url_for('admins.admin'))
            else:
                # TODO: need to fix to student welcome page
                return redirect(url_for('users.welcome_teacher'))

        elif user and not (form.password.data == user.password):
            flash("Please check your login detail and try again!")
            logging.warning('SECURITY - USER FAILED LOGIN ATTEMPT|%s|%s|%s', user.UID, user.email,
                            request.remote_addr)
        else:
            flash("Please check your login detail and try again!")

    return render_template('login.html', form=form)


# Logs the user out of the system
# Author: Harry Sayer
@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - USER LOG OUT|%s|%s|%s', current_user.UID, current_user.email,
                    request.remote_addr)
    logout_user()
    return render_template('index.html')


# Teacher welcome view
# Author: Jiayuan Zhang
@users_blueprint.route('/welcome_teacher')
@login_required
@requires_roles('teacher')
def welcome_teacher():
    return render_template('teacher-welcome.html', name=current_user.firstName)


# Profile view
# Author: Jiayuan Zhang
@users_blueprint.route('/profile')
@login_required
@requires_roles('teacher', 'student')
def profile():
    return render_template('profile.html', firstName=current_user.firstName, surname=current_user.surname,
                           email=current_user.email, id=current_user.UID,
                           school=School.query.filter_by(ID=current_user.schoolID).first().schoolName)


# Change password
# Author: Jiayuan Zhang
@users_blueprint.route('/change-password', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher', 'student')
def change_password():
    # create change password form object
    form = ChangePasswordForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get current user
        user = User.query.filter_by(email=current_user.email).first()
        if form.old_password.data == user.password:
            # update new password to database
            user.password = form.new_password.data
            db.session.commit()
            # successfully updated, log out
            logout_user()
            # send user to login page
            return redirect(url_for('users.login'))
        else:
            flash('Your password is not correct.')
            render_template('change-password.html', form=form)

    # if request method is GET or form not valid re-render signup page
    return render_template('change-password.html', form=form)


# Student Info view, display all students
# Author: Jiayuan Zhang
@users_blueprint.route('/student_info')
@login_required
@requires_roles('teacher')
def student_info():
    # get all students in the same school of current teacher
    users = User.query.filter_by(schoolID=current_user.schoolID).all()
    students = []
    for s in users:
        if s.role == "student":
            students.append(s)

    # get current teacher school
    school = School.query.filter_by(ID=current_user.schoolID).first().schoolName

    return render_template('student-info.html', students=students, school=school)


# View all grades of a specific student
# Author: Jiayuan Zhang
@users_blueprint.route('/student_info/results', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def student_results():
    # get student
    if request.method == 'POST':
        email = request.form.get('student_email')
    student = User.query.filter_by(email=email).first()

    # get all results of this student
    results = []
    take = Take.query.filter_by(email=email).all()
    for t in take:
        # prepare the information
        assignment = Assignment.query.filter_by(AID=t.AID).first()
        assignment_name = assignment.assignmentName
        course = assignment.CID
        grade = t.grade
        # create a dictionary to store the information
        list_item = {"assignment": assignment_name,
                     "course": course,
                     "grade": grade}

        results.append(list_item)

    return render_template('student-result.html', student=student, results=results)
