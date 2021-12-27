from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from courses.forms import CourseForm
from models import Course, Engage, User

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
def create_courses():
    form = CourseForm()
    form.added_students.choices = get_students()

    if form.validate_on_submit():
        new_course = Course(coursename=form.course_name.data)
        db.session.add(new_course)
        db.session.commit()

        add_teacher = Engage(email=current_user.email, CID=new_course.CID)
        db.session.add(add_teacher)
        db.session.commit()

        for student in form.added_students.data:
            add_student = Engage(email=student, CID=new_course.CID)
            db.session.add(add_student)

        db.session.commit()

        # commented out since there is no hot-bar
        # return courses()
        flash('Your course %s has been created.' % new_course.courseName)

    return render_template('create-courses.html', form=form)


def get_students():
    students_of_school = User.query.filter_by(role="student", schoolID=current_user.schoolID).all()

    choices = []
    for student in students_of_school:
        tup = (student.email, str(student.email + ": " + student.firstName + " " + student.surname))
        choices.append(tup)

    return choices
