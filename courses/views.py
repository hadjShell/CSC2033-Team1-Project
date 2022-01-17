# IMPORTS
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db, login_required, requires_roles, ROOT_DIR
from courses.forms import CourseForm, JoinForm
from models import Course, Engage, User, Assignment, Create

"""
This python file handles the views and activities related to course.
-------------------------------------------------------------------------------------------------------------------
Created by Jiayuan Zhang
"""

# CONFIG
courses_blueprint = Blueprint('courses', __name__, template_folder='templates')


# HELP METHOD
# get all course ID
def get_courses():
    courses = Course.query.all()
    courses_ids = []
    for c in courses:
        courses_ids.append(c.CID)
    return courses_ids


# get all course id a teacher engaged
def get_courses_teacher():
    engage = Engage.query.filter_by(email=current_user.email).all()
    courses_ids = []
    for e in engage:
        courses_ids.append(e.CID)
    return courses_ids


# VIEWS
# Courses page view
# Author: Jiayuan Zhang
@courses_blueprint.route('/courses')
@login_required
@requires_roles('teacher', 'student')
def courses():
    # get all courses belonging to current user
    engaged = Engage.query.filter_by(email=current_user.email).all()
    engaged_courses = []
    for e in engaged:
        engaged_courses.append(Course.query.filter_by(CID=e.CID).first())

    # get user role
    role = current_user.role

    # render course page with engaged courses
    return render_template('course.html', engaged_courses=engaged_courses, role=role)


# View the class list of a specific course
# Author: Jiayuan Zhang
@courses_blueprint.route('/courses/classlist', methods=['GET', 'POST'])
@login_required
@requires_roles('teacher')
def course_classlist():
    # get course id
    if request.method == 'POST':
        course_id = request.form.get('class_list')

    # get course name
    course_name = Course.query.filter_by(CID=course_id).first().courseName

    # get class list
    class_list = []
    engaged = Engage.query.filter_by(CID=course_id).all()
    for e in engaged:
        class_list.append(User.query.filter_by(email=e.email).first())
    for s in class_list:
        if s.role == "teacher":
            class_list.remove(s)

    return render_template('course-classlist.html', course_id=course_id, course_name=course_name, class_list=class_list)


# View all assignments of a course
# Author: Jiayuan Zhang
@courses_blueprint.route('/courses/assignments', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher', 'student')
def course_assignments():
    # get course id
    if request.method == 'POST':
        course_id = request.form.get('assignments_list')

    # get all assignments of this course
    assignments = Assignment.query.filter_by(CID=course_id).all()

    return render_template('course-assignmentlist.html', course_id=course_id, assignments=assignments,
                           role=current_user.role)


# Current teacher creates a course under his or her govern
# Author: Jiayuan Zhang
@courses_blueprint.route('/courses/create-course', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def create_course():
    # create course form object
    form = CourseForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # if already have this course
        if Course.query.filter_by(CID=form.course_id.data).first():
            flash('This course is already existed!')
            return render_template('create-course.html', form=form)
        else:
            # create a new course object and a engage object
            new_course = Course(CID=form.course_id.data, courseName=form.course_name.data)
            new_engage = Engage(email=current_user.email, CID=form.course_id.data)
            # add to database
            db.session.add(new_course)
            db.session.add(new_engage)
            db.session.commit()
            # create course folder
            path = ROOT_DIR / Path("static/teachers_submission/" + str(form.course_id.data))
            path.mkdir(parents=True, exist_ok=True)
            # send user to course page
            return redirect(url_for('courses.courses'))

    # if request method is GET or form not valid re-render create course page
    return render_template('create-course.html', form=form)


# Current teacher joins a course
# Author: Jiayuan Zhang
@courses_blueprint.route('/courses/join-course', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def join_course():
    # create course form object
    form = JoinForm()
    form.course_id.choices = get_courses()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        course_id = form.course_id.data
        # if course doesn't exist
        if not Course.query.filter_by(CID=course_id).first():
            flash('There is no such course in the system!')
            return render_template('join-course.html', form=form)
        # if already joined
        if Engage.query.filter_by(CID=course_id, email=current_user.email).first():
            flash('You have already joined the course')
            return render_template('join-course.html', form=form)
        else:
            # create a new engage object
            new_engage = Engage(email=current_user.email, CID=course_id)
            db.session.add(new_engage)

            # create new create objects
            assignments = Assignment.query.filter_by(CID=course_id).all()
            for a in assignments:
                new_create = Create(email=current_user.email, AID=a.AID)
                db.session.add(new_create)

            # commit db change
            db.session.commit()

            # successful message
            flash('You have joined the course successfully!')
            return render_template('join-course.html', form=form)

    # if request method is GET or form not valid re-render join course page
    return render_template('join-course.html', form=form)
