# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user
import logging
from app import db, login_required, requires_roles, ROOT_DIR
from models import User, School, Take, Assignment, Engage, Course
from users.forms import LoginForm, RegisterForm, ChangePasswordForm, AddStudentForm, GradeForm
from courses.views import get_courses
from werkzeug.security import check_password_hash
from pathlib import Path

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
# Authors: Uzair Yousaf, Harry Sayer, Jiayuan Zhang
@users_blueprint.route('/register', methods=['GET', 'POST'])
@requires_roles('student')
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
                        role=form.role.data,
                        password=form.password.data,
                        schoolID=form.schoolID.data,
                        firstName=form.firstName.data,
                        surname=form.lastName.data,
                        UID=form.UID.data,
                        approved=False)
#
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # create submission folder
        path = ROOT_DIR / Path("static/students_submission/" + str(form.email.data))
        path.mkdir(parents=True, exist_ok=True)

        logging.warning('SECURITY - USER REGISTRATION|%s|%s|%s', new_user.UID, new_user.email,
                        request.remote_addr)

        # sends user to login page
        return redirect((url_for('users.profile')))
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
        if user and check_password_hash(user.password, form.password.data) and user.approved is True:
            login_user(user)

            logging.warning('SECURITY - USER LOG IN|%s|%s|%s', current_user.UID, current_user.email,
                            request.remote_addr)

            # Go to welcome page based on role
            if current_user.role == 'admin':
                return redirect(url_for('admins.admin'))
            else:
                return redirect(url_for('users.welcome'))

        elif user and not check_password_hash(user.password, form.password.data) and user.approved is True:
            flash("Please check your login detail and try again!")
            logging.warning('SECURITY - USER FAILED LOGIN ATTEMPT|%s|%s|%s', user.UID, user.email,
                            request.remote_addr)
        elif user and check_password_hash(user.password, form.password.data) and user.approved is False:
            return render_template('errors/waiting-approval.html')

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


# Welcome view
# Author: Jiayuan Zhang
@users_blueprint.route('/welcome')
@login_required
@requires_roles('teacher', 'student')
def welcome():
    if current_user.role == 'teacher':
        return render_template('teacher-welcome.html', name=current_user.firstName)
    else:
        return render_template('student-welcome.html', name=current_user.firstName)


# Profile view
# Author: Jiayuan Zhang
@users_blueprint.route('/profile')
@login_required
@requires_roles('teacher', 'student')
def profile():
    return render_template('profile.html', firstName=current_user.firstName, surname=current_user.surname,
                           email=current_user.email, id=current_user.UID,
                           school=School.query.filter_by(ID=current_user.schoolID).first().schoolName,
                           role=current_user.role)


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

    # if request method is GET or form not valid re-render change password page
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


# add student to a course
# Author: Jiayuan Zhang
@users_blueprint.route('/courses/add-student', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def add_student():
    # create a AddStudentForm object
    form = AddStudentForm()
    form.course_id.choices = get_courses()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get student email and course id
        student_email = form.student_email.data
        course_id = form.course_id.data
        # if student doesn't exist
        if not User.query.filter_by(email=student_email).first():
            flash('Student doesn\'t exist!')
            return render_template('add-student.html', form=form)
        # if course doesn't exist
        if not Course.query.filter_by(CID=course_id).first():
            flash('Course doesn\'t exist!')
            return render_template('add-student.html', form=form)
        # if student is already in the course
        if Engage.query.filter_by(email=student_email, CID=course_id).first():
            flash('Student is already in the course!')
            return render_template('add-student.html', form=form)
        else:
            # create a new engage object
            new_engage = Engage(email=student_email, CID=course_id)
            db.session.add(new_engage)
            # create submission folder
            path = ROOT_DIR / Path("static/students_submission/" + student_email + "/" + course_id)
            path.mkdir(parents=True, exist_ok=True)

            # get all assignments of that course
            assignments = Assignment.query.filter_by(CID=course_id).all()
            # create new take objects
            for a in assignments:
                new_take = Take(email=student_email, AID=a.AID, submitTime=None, grade=None)
                db.session.add(new_take)

            # commit db change
            db.session.commit()

            # successful message
            flash('You have added the student successfully!')
            return render_template('add-student.html', form=form)

    # if request method is GET or form not valid re-render add student page
    return render_template('add-student.html', form=form)


# teacher download student submit file,
# assume file exists, otherwise unseen
# Author: Jiayuan Zhang
@users_blueprint.route('/download-answer', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def download_answer():
    # get assignment id and student email
    if request.method == 'POST':
        student_email = request.form.get('student_email')
        assignment_id = request.form.get('assignment_id')
        assignment_cid = request.form.get('assignment_cid')

    # get directory
    directory = ROOT_DIR / Path("static/students_submission/" + student_email + "/" + assignment_cid)
    # get filename
    filename = Take.query.filter_by(email=student_email, AID=assignment_id).first().doc_name

    return send_from_directory(directory, filename)


# teacher grade student
# Author: Jiayuan Zhang
@users_blueprint.route('/grade', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def grade():
    # create grade form
    form = GradeForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get student email and assignment id
        student_email = form.student_email.data
        assignment_id = form.assignment_id.data

        # get take
        take = Take.query.filter_by(email=student_email, AID=assignment_id).first()

        if take:
            # if already grade
            if take.grade:
                flash('Student has already been graded!')
                return render_template('grade.html', form=form)
            else:
                take.grade = form.grade.data
                db.session.commit()
                flash('Success!')
                return render_template('grade.html', form=form)
        else:
            flash("Student doesn't take the assignment!")
            return render_template('grade.html', form=form)

    # if request method is GET or form not valid re-render grade page
    return render_template('grade.html', form=form)
