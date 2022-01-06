from flask import Blueprint, render_template, flash, request
from app import db, login_required, requires_roles
from models import School, User

administrator_blueprint = Blueprint('admins', __name__, template_folder='templates')


# VIEW
# Author: Harry Sayer
@administrator_blueprint.route('/admin', methods=['POST', 'GET'])
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

    return render_template('admin.html', all_users=users)


# gets all the schools that exist within the database
# Author: Harry Sayer
@administrator_blueprint.route('/view-all-schools', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_school():
    return render_template('admin.html', all_schools=School.query.all())


# allows the admin to create schools
# Author: Harry Sayer
@administrator_blueprint.route('/create-school', methods=['POST', 'GET'])
@login_required
@requires_roles('admin')
def create_school():
    # input from the admin
    name = request.form.get('name')
    name.strip()

    # if the school already exists or field is left blank it is then it is not created
    if (len(School.query.filter_by(schoolName=name).all())) == 0 and (len(name) > 0):
        new_school = School(schoolName=name)
        db.session.add(new_school)
        db.session.commit()

        flash('The school "%s" has been created' % name)
        return render_template('admin.html')

    # checks to make sure the entered school doesn't already exist
    # if the length of list is greater than 0 obviously school exists in the table
    elif len(School.query.filter_by(schoolName=name).all()) > 0:
        flash('The school "%s" already exists' % name)
        return render_template('admin.html')

    else:
        flash('Field was left blank')
        return admin()


# Function that allows the admin to approve of user registration, either approving or declining it
# Author: Harry Sayer
@administrator_blueprint.route('/approve', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def approve_user():
    if request.method == 'POST':

        # whether the approve or decline button has been pressed
        approved = request.form.get("approve")
        declined = request.form.get("decline")

        if approved is not None:
            user = User.query.filter_by(email=approved).first()
            # approves the user - no longer needs to be reviewed and can access page
            user.approved = True
            db.session.commit()
            flash(user.firstName + " " + user.surname + " has been approved of registration")

        elif declined is not None:
            user = User.query.filter_by(email=declined).first()
            # when user is declined they are deleted from the database
            User.query.filter_by(UID=user.UID).delete()
            db.session.commit()
            flash(user.firstName + " " + user.surname + " has been declined of registration")

    # gets all the current unapproved users
    to_approve = []
    all_users = User.query.filter_by(approved=False)
    for user in all_users:
        # gets the name of the school the user attends
        their_school = School.query.filter_by(ID=user.schoolID).first()
        to_approve.append((user, their_school))
    return render_template('approve.html', to_be_approved=to_approve)


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

    return render_template('admin.html', logs=all_logs)
