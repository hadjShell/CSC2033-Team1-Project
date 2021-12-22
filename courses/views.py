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
        get_course = Course.query.filter_by(CID=course.CID).first()
        user_courses.append(get_course)

    return render_template('course.html', course_list=user_courses)


@courses_blueprint.route('/create-courses', methods=['POST', 'GET'])
def createCourses():
    form = CourseForm()

    # couldn't get form.validate_on_submit() to return true so using this as a way to write the name into the db
    if form.course_name.data is not None:

        new_course = Course(coursename=form.course_name.data)
        db.session.add(new_course)

        new_engage = Engage(email=current_user.email, CID=new_course.CID)
        db.session.add(new_engage)

        db.session.commit()

        return courses()

    return render_template('create-courses.html', form=form)
