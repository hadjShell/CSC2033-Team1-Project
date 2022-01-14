# IMPORTS
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user
from app import db, login_required, requires_roles
from models import School, User, Assignment, Course, Engage
from administrator.forms import CreateSchoolForm

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
                teachers.append(user.schoolID)

        # get course set
        course = (c.CID, c.courseName, teachers)
        courses.append(course)

    return render_template('', all_courses=courses)


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


# Function that allows the admin to approve of user registration, either approving or declining it
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
