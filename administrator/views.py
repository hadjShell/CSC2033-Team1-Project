from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db, requires_roles
from models import School, User


administrator_blueprint = Blueprint('admins', __name__, template_folder='templates')


@administrator_blueprint.route('/admin', methods=['POST', 'GET'])
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')


# gets all users of the database, excluding the admin
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
@administrator_blueprint.route('/view-all-schools', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_school():
    return render_template('admin.html', all_schools=School.query.all())


# allows the admin to create schools
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

    elif len(School.query.filter_by(schoolName=name).all()) > 0:
        flash('The school "%s" already exists' % name)
        return render_template('admin.html')

    else:
        flash('Field was left blank')
        return admin()


@administrator_blueprint.route('/approve', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def approve_user():
    if request.method == 'POST':

        approved = request.form.get("approve")
        declined = request.form.get("decline")

        if approved is not None:
            user = User.query.filter_by(email=approved).first()
            user.approved = True
            db.session.commit()
            flash(user.firstName + " " + user.surname + " has been approved of registration")

        elif declined is not None:
            user = User.query.filter_by(email=declined).first()
            User.query.filter_by(UID=user.UID).delete()
            db.session.commit()
            flash(user.firstName + " " + user.surname + " has been declined of registration")

    to_approve = []
    all_users = User.query.filter_by(approved=False)
    for user in all_users:
        their_school = School.query.filter_by(ID=user.schoolID).first()
        to_approve.append((user, their_school))
    return render_template('approve.html', to_be_approved=to_approve)

