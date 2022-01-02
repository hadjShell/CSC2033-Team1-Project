from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from models import School, User


administrator_blueprint = Blueprint('admins', __name__, template_folder='templates')


@administrator_blueprint.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


# gets all users of the database, excluding the admin
@administrator_blueprint.route('/view-all-users', methods=['POST'])
def view_all_users():

    users = []
    for cur in User.query.all():
        # admin is not appended to the list
        if cur.role == "admin":
            continue
        else:
            user_school = School.query.filter_by(ID=cur.schoolID).first()
            user = (cur.email, cur.firstName, cur.surname, cur.role, user_school.schoolName, cur.UID)
            users.append(user)

    return render_template('admin.html', all_users=users)


# gets all the schools that exist within the database
@administrator_blueprint.route('/view-all-schools', methods=['POST'])
def view_all_school():
    return render_template('admin.html', all_schools=School.query.all())


# allows the admin to create schools
@administrator_blueprint.route('/create-school', methods=['POST', 'GET'])
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
