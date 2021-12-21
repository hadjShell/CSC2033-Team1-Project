from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from app import db
from courses.forms import CourseForm
from models import Course, Engage

courses_blueprint = Blueprint('courses', __name__, template_folder='templates')


# displays all the courses the user is a part of
@courses_blueprint.route('/courses', methods=['POST', 'GET'])
def courses():
    get_courses = Engage.query.filter_by(email=current_user.email).all()

    user_courses = []
    for course in get_courses:
        get_course = Course.query.filter_by(CID=course.CID)
        user_courses.append(get_course)

    return render_template('course.html', course_list=user_courses)


@courses_blueprint.route('/create-courses', methods=['GET', 'POST'])
def createCourses():
    form = CourseForm()

    if form.validate_on_submit():
        latest_course = Course.query.filter_by(desc('CID')).first()

        new_course = Course(CID=latest_course+1, courseName=form.course_name.data)
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('users.welcome_teacher'))

    return render_template('course.html', form=form)
