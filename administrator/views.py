# IMPORTS
from pathlib import Path
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user
from app import db, login_required, requires_roles, ROOT_DIR
from models import School, User, Assignment, Course, Engage, Create, Take
from administrator.forms import CreateSchoolForm, AddPeopleForm
from courses.forms import CourseForm
from courses.views import get_courses

# CONFIG
administrator_blueprint = Blueprint('admins', __name__, template_folder='templates')


# VIEW
# Home page view
# Author: Harry Sayer
@administrator_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')


# gets all users of the database, excluding the admin
# Author: Harry Sayer
@administrator_blueprint.route('/view-all-users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
    users = []
    for cur in User.query.all():
        # admin is not appended to the list
        if cur.role == "admin":
            continue
        else:
            user_school = School.query.filter_by(ID=cur.schoolID).first()
            user = (cur.UID, cur.email, cur.firstName, cur.surname, cur.role, user_school.schoolName,
                    ("Approved" if cur.approved is True else "Needs Review"))
            users.append(user)

    return render_template('', all_users=users)


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
    return render_template('', all_assignments=Assignment.query.all())


# gets all the schools that exist within the database
# Author: Harry Sayer
@administrator_blueprint.route('/view-all-schools')
@login_required
@requires_roles('admin')
def view_all_schools():
    return render_template('admin-schools.html', schools=School.query.all())


# allows the admin to create schools
# Author: Harry Sayer
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


# Function that allows the admin to approve of user registration
# Author: Harry Sayer
@administrator_blueprint.route('/approve', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def approve_user():
    if request.method == 'POST':

        # whether the approve or decline button has been pressed
        approved = request.form.get("approve")

        if approved is not None:
            user = User.query.filter_by(email=approved).first()
            # approves the user - no longer needs to be reviewed and can access page
            user.approved = True
            db.session.commit()
            flash(user.firstName + " " + user.surname + " has been approved of registration")

    return render_template('approve.html', to_be_approved=get_unapproved_members())


# Function that allows the admin to decline of user registration
# Author: Harry Sayer
@administrator_blueprint.route('/decline', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def decline_user():

    if request.method == 'POST':

        # whether the approve or decline button has been pressed
        declined = request.form.get("decline")

        if declined is not None:
            user = User.query.filter_by(email=declined).first()
            # when user is declined they are deleted from the database
            User.query.filter_by(UID=user.UID).delete()
            db.session.commit()
            flash(user.firstName + " " + user.surname + " has been declined of registration")

    return render_template('approve.html', to_be_approved=get_unapproved_members())


# gets all the current unapproved users
# Author: Harry Sayer
def get_unapproved_members():
    to_approve = []
    all_users = User.query.filter_by(approved=False)
    for user in all_users:
        # gets the name of the school the user attends
        their_school = School.query.filter_by(ID=user.schoolID).first()
        to_approve.append((user, their_school))
    return to_approve


# Displays all the security logs to the admin
# Author: Harry Sayer
@administrator_blueprint.route('/security-logs', methods=['POST'])
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

    return render_template('', logs=all_logs)


# Displays all assignments to the admin and allows the admin to delete the assignment and all the relations to that
# assignment.
# Author: Harry Sayer
@administrator_blueprint.route('/delete-assignment', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def delete_assignment():

    selected_assignment = request.form.get('delete')

    if selected_assignment is not None:
        assignment_to_delete = Assignment.query.filter_by(AID=int(selected_assignment)).first()
        Assignment.query.filter_by(AID=assignment_to_delete.AID).delete()
        db.session.commit()
        flash("Assignment with ID: " + selected_assignment + " has been deleted.")

    return render_template('admins.html', all_assignments=Assignment.query.all())
