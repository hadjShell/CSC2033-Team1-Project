# IMPORTS
import os
from pathlib import Path
from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app import db, login_required, requires_roles, ROOT_DIR
from models import School, User, Assignment, Course, Engage, Create, Take
from administrator.forms import CreateSchoolForm, AddPeopleForm, UpdateCourseForm, DeleteCourseForm, \
    UpdateAssignmentForm, DeleteAssignmentForm, ApproveForm
from courses.forms import CourseForm
from courses.views import get_courses
from assignments.views import get_assignments, allowed_file

"""
This python file handles the views and operations of admin users.
-------------------------------------------------------------------------------------------------------------------
Created by Jiayuan Zhang, Harry Sayer
"""

# CONFIG
administrator_blueprint = Blueprint('admins', __name__, template_folder='templates')


# HELP FUNCTION
# get all unapproved user email
# Author: Jiayuan Zhang
def get_unapproved():
    unapproved = []
    for user in User.query.filter_by(approved=False).all():
        unapproved.append(user.email)
    return unapproved


# VIEW
# Home page view
# Author: Harry Sayer
@administrator_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')


# gets all users of the database
# Author: Harry Sayer, Jiayuan Zhang
@administrator_blueprint.route('/view-all-users', methods=['POST', 'GET'])
@login_required
@requires_roles('admin')
def view_all_users():
    users = []
    for u in User.query.all():
        school = School.query.filter_by(ID=u.schoolID).first().schoolName
        user = (u.email, school, u.role, u.UID, u.firstName, u.surname, u.approved)
        users.append(user)
    return render_template('admin-users.html', users=users)


# gets all the courses that exist within the database
# Author: Jiayuan Zhang
@administrator_blueprint.route('/view-all-courses')
@login_required
@requires_roles('admin')
def view_all_courses():
    courses = []
    for c in Course.query.all():
        # get engaged teachers
        teachers = []
        engage = Engage.query.filter_by(CID=c.CID).all()
        for e in engage:
            user = User.query.filter_by(email=e.email).first()
            if user.role == 'teacher':
                teachers.append(user.firstName + ' ' + user.surname)

        # get course set
        course = (c.CID, c.courseName, teachers)
        courses.append(course)

    return render_template('admin-courses.html', courses=courses)


# gets all the assignments that exist within the database
# Author: Jiayuan Zhang
@administrator_blueprint.route('/view-all-assignments')
@login_required
@requires_roles('admin')
def view_all_assignments():
    assignments = Assignment.query.all()
    return render_template('admin-assignments.html', assignments=assignments)


# gets all the schools that exist within the database
# Author: Harry Sayer
@administrator_blueprint.route('/view-all-schools')
@login_required
@requires_roles('admin')
def view_all_schools():
    return render_template('admin-schools.html', schools=School.query.all())


# allows the admin to create schools
# Author: Jiayuan Zhang
@administrator_blueprint.route('/create-school', methods=['POST', 'GET'])
@login_required
@requires_roles('admin')
def create_school():
    form = CreateSchoolForm()

    if form.validate_on_submit():
        # if school is already exist
        if School.query.filter_by(schoolName=form.schoolName.data).first():
            flash('School is already existed!')
            return render_template('admin-create-school.html', form=form)
        else:
            # create new school object
            new_school = School(schoolName=form.schoolName.data)
            db.session.add(new_school)
            db.session.commit()
            flash('Success!')

    return render_template('admin-create-school.html', form=form)


# Create Course
# Author: Jiayuan Zhang
@administrator_blueprint.route('/admin/create-course', methods=['POST', 'GET'])
@login_required
@requires_roles('admin')
def create_course():
    # create course form object
    form = CourseForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # if already have this course
        if Course.query.filter_by(CID=form.course_id.data).first():
            flash('This course is already existed!')
            return render_template('admin-create-course.html', form=form)
        else:
            # create a new course object
            new_course = Course(CID=form.course_id.data, courseName=form.course_name.data)
            # add to database
            db.session.add(new_course)
            db.session.commit()
            # create course folder
            path = ROOT_DIR / Path("static/teachers_submission/" + str(form.course_id.data))
            path.mkdir(parents=True, exist_ok=True)
            # send user to course page
            return redirect(url_for('admins.view_all_courses'))

    # if request method is GET or form not valid re-render create course page
    return render_template('admin-create-course.html', form=form)


# Add teacher or student to a course
# Author: Jiayuan Zhang
@administrator_blueprint.route('/admin/add-people', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def add_people():
    form = AddPeopleForm()
    form.course_id.choices = get_courses()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        course_id = form.course_id.data
        user_email = form.email.data
        # if course doesn't exist
        if not Course.query.filter_by(CID=course_id).first():
            flash('There is no such course in the system!')
            return render_template('admin-add-people.html', form=form)
        # if user not exist
        if not User.query.filter_by(email=user_email).first():
            flash('There is no such user in the system!')
            return render_template('admin-add-people.html', form=form)
        # if already joined
        if Engage.query.filter_by(CID=course_id, email=user_email).first():
            flash('You have already joined the course')
            return render_template('admin-add-people.html', form=form)
        else:
            role = User.query.filter_by(email=user_email).first().role
            # create a new engage object
            new_engage = Engage(email=user_email, CID=course_id)
            db.session.add(new_engage)
            db.session.commit()

            assignments = Assignment.query.filter_by(CID=course_id).all()
            # if user is a teacher
            if role == 'teacher':
                # create new create objects
                for a in assignments:
                    new_create = Create(email=user_email, AID=a.AID)
                    db.session.add(new_create)
                # commit db change
                db.session.commit()
            # if user is a student
            else:
                # create new take objects
                for a in assignments:
                    new_take = Take(email=user_email, AID=a.AID, submitTime=None, grade=None)
                    db.session.add(new_take)
                db.session.commit()
                # create folder
                path = ROOT_DIR / Path("static/students_submission/" + user_email + "/" + course_id)
                path.mkdir(parents=True, exist_ok=True)

            # successful message
            flash('Success!')
            return render_template('admin-add-people.html', form=form)

    # if request method is GET or form not valid re-render join course page
    return render_template('admin-add-people.html', form=form)


# Update a course
# Author: Jiayuan Zhang
@administrator_blueprint.route('/admin/update-course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update_course():
    form = UpdateCourseForm()
    form.course_id.choices = get_courses()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # update course name
        new_course_name = form.new_course_name.data
        course = Course.query.filter_by(CID=form.course_id.data).first()
        course.courseName = new_course_name
        db.session.commit()

        # successful message
        flash('Success!')
        return render_template('admin-update-course.html', form=form)

    # if request method is GET or form not valid re-render join course page
    return render_template('admin-update-course.html', form=form)


# Delete a course
# Author: Jiayuan Zhang
@administrator_blueprint.route('/admin/delete-course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def delete_course():
    form = DeleteCourseForm()
    form.course_id.choices = get_courses()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get course id
        course_id = form.course_id.data
        # delete all engage entities
        Engage.query.filter_by(CID=course_id).delete()
        db.session.commit()
        # get assignments in the course
        assignments = Assignment.query.filter_by(CID=course_id).all()
        # delete all create and take entities
        for a in assignments:
            Create.query.filter_by(AID=a.AID).delete()
            Take.query.filter_by(AID=a.AID).delete()
        db.session.commit()
        # delete all assignment entities
        Assignment.query.filter_by(CID=course_id).delete()
        db.session.commit()
        # delete course
        Course.query.filter_by(CID=course_id).delete()
        db.session.commit()

        # send user to course page
        return redirect(url_for('admins.view_all_courses'))

    # if request method is GET or form not valid re-render delete course page
    return render_template('admin-delete-course.html', form=form)


# Update an assignment file
# Author: Jiayuan Zhang
@administrator_blueprint.route('/admin/update-assignment', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update_assignment():
    form = UpdateAssignmentForm()
    form.assignment.choices = get_assignments()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get assignment
        assignment_id = int(form.assignment.data.split(' ')[0])
        assignment = Assignment.query.filter_by(AID=assignment_id).first()
        # get uploaded file
        file = form.new_file.data
        filename = secure_filename(file.filename)
        # If file is allowed
        if allowed_file(file.filename):
            # delete old file
            os.remove(ROOT_DIR / Path(assignment.doc_path))
            # update assignment doc_name and doc_path
            assignment.doc_name = filename
            assignment.doc_path = "static/teachers_submission/" + assignment.CID + "/" + filename
            db.session.commit()
            # update file
            file.save(ROOT_DIR / Path(assignment.doc_path))

            # successful message
            flash('Success!')
            return render_template('admin-update-assignment.html', form=form)

        # if file is not allowed
        else:
            flash('File extension is not allowed!')
            return render_template('admin-update-assignment.html', form=form)

    # if request method is GET or form not valid re-render update assignment page
    return render_template('admin-update-assignment.html', form=form)


# Delete an assignment
# Author: Jiayuan Zhang
@administrator_blueprint.route('/admin/delete-assignment', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def delete_assignment():
    form = DeleteAssignmentForm()
    form.assignment.choices = get_assignments()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get assignment id
        assignment_id = int(form.assignment.data.split(' ')[0])

        # delete all create and take entities
        Create.query.filter_by(AID=assignment_id).delete()
        Take.query.filter_by(AID=assignment_id).delete()
        db.session.commit()
        # delete assignment entity
        Assignment.query.filter_by(AID=assignment_id).delete()
        db.session.commit()

        # send user to assignment page
        return redirect(url_for('admins.view_all_assignments'))

    # if request method is GET or form not valid re-render delete assignment page
    return render_template('admin-delete-assignment.html', form=form)


# Function that allows the admin to approve of user registration, either approving or declining it
# Author: Harry Sayer, Jiayuan Zhang
@administrator_blueprint.route('/admin/approve', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def approve_user():
    form = ApproveForm()
    form.email.choices = get_unapproved()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # get user email and decision
        email = form.email.data
        decision = form.decision.data
        # if approved
        if decision == "Yes":
            # set approved
            user = User.query.filter_by(email=email).first()
            user.approved = True
            db.session.commit()

            # successful message
            flash('Success!')
            return render_template('admin-approve.html', form=form)
        else:
            # delete user
            User.query.filter_by(email=email).delete()
            db.session.commit()

            # successful message
            flash('Success!')
            return render_template('admin-approve.html', form=form)

    # if request method is GET or form not valid re-render approve page
    return render_template('admin-approve.html', form=form)


# Displays all the security logs to the admin
# Author: Harry Sayer
@administrator_blueprint.route('/security-logs')
@requires_roles('admin')
@login_required
def security_log():
    with open("Odin.log", "r") as file:
        contents = file.read().splitlines()
        contents.reverse()

    # splitting the log string into separate parts to display as a table in the html
    all_logs = []
    for log in contents:
        chop = log.split('|')
        all_logs.append(chop)

    return render_template('admin-log.html', logs=all_logs)
