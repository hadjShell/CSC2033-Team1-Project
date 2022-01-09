# IMPORTS
import datetime
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user
from app import db, login_required, requires_roles
from assignments.forms import AssignmentForm
from models import Assignment, Create, Take, User, Engage
from courses.views import get_courses
from app import ALLOWED_EXTENSIONS, ROOT_DIR
from werkzeug.utils import secure_filename


# CONFIG
assignments_blueprint = Blueprint('assignments', __name__, template_folder='templates')


# HELP FUNCTIONS
# A function that returns the 'deadline' value
def deadlineValue(a):
    return a.deadline


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# VIEW
# Assignment page view
# Author: Jiayuan Zhang
@assignments_blueprint.route('/assignments')
@login_required
@requires_roles('teacher', 'student')
def assignments():
    # get user role
    role = current_user.role
    # get all assignments belonging to current user
    assignments = []
    if role == "teacher":
        create = Create.query.filter_by(email=current_user.email).all()
        for c in create:
            assignments.append(Assignment.query.filter_by(AID=c.AID).first())
    else:
        take = Take.query.filter_by(email=current_user.email).all()
        for t in take:
            assignments.append(Assignment.query.filter_by(AID=t.AID).first())

    # sort assignments by deadline
    assignments.sort(key=deadlineValue)

    # render assignment page
    return render_template('assignment.html', assignments=assignments, role=role)


# View all students who take the assignment and relative information
# Author: Jiayuan Zhang
@assignments_blueprint.route('/assignments/detail', methods=('GET', 'POST'))
@login_required
@requires_roles('teacher')
def assignments_detail():
    # get assignment
    if request.method == 'POST':
        assignment_id = request.form.get('assignmentID')
        assignment = Assignment.query.filter_by(AID=assignment_id).first()

    # get all students who take the assignment
    students_take_assignment = []
    take = Take.query.filter_by(AID=assignment_id).all()
    for t in take:
        students_take_assignment.append(User.query.filter_by(email=t.email).first())

    # create a list that used to show relative information
    assignment_student_list = []
    for s in students_take_assignment:
        # prepare the information
        take = Take.query.filter_by(email=s.email, AID=assignment_id).first()
        submit_time = take.submitTime
        grade = take.grade
        # create a dictionary that included the information
        list_item = {"schoolID": s.schoolID,
                     "name": s.firstName + ' ' + s.surname,
                     "submitTime": submit_time,
                     "grade": grade}

        assignment_student_list.append(list_item)

    return render_template('assignment-detail.html', assignment=assignment, list=assignment_student_list)


# Function to create an assignment
# Author: Jiayuan Zhang, Tom Dawson
@assignments_blueprint.route('/assignments/create-assignment', methods=['POST', 'GET'])
@login_required
@requires_roles('teacher')
def create_assignment():
    # create an assignment form
    form = AssignmentForm()
    form.assignmentCID.choices = get_courses()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # if already have this assignment
        if Assignment.query.filter_by(assignmentName=form.assignmentTitle.data, CID=form.assignmentCID.data).first():
            flash('This assignment is already existed!')
            return render_template('create-assignment.html', form=form)
        else:
            # get uploaded file
            file = form.assignmentFile.data
            filename = secure_filename(file.filename)
            # If file is allowed
            if allowed_file(file.filename):
                # get secured file name and save file
                data_folder = Path("static/uploads/" + str(form.assignmentCID.data) + '/' + filename)
                file.save(ROOT_DIR / data_folder)
                # composite date and time
                combined_date = datetime.datetime(form.assignmentDeadlineDay.data.year,
                                                  form.assignmentDeadlineDay.data.month,
                                                  form.assignmentDeadlineDay.data.day,
                                                  form.assignmentDeadlineTime.data.hour,
                                                  form.assignmentDeadlineTime.data.minute)
                # create new assignment object
                assignment_number = len(Assignment.query.all())
                new_assignment = Assignment(AID=assignment_number + 1,
                                            assignmentName=form.assignmentTitle.data,
                                            description=form.assignmentDescription.data,
                                            deadline=combined_date,
                                            CID=form.assignmentCID.data,
                                            doc_name=filename,
                                            doc_path='/static/uploads/' + form.assignmentCID.data + '/' + filename)
                db.session.add(new_assignment)
                # create new create object
                new_create = Create(email=current_user.email, AID=new_assignment.AID)
                db.session.add(new_create)
                # get all students engaged in the course
                user_in_course = Engage.query.filter_by(CID=form.assignmentCID.data).all()
                students_in_course = []
                for u in user_in_course:
                    user = User.query.filter_by(email=u.email).first()
                    if user.role == 'student':
                        students_in_course.append(user)
                # create new take objects
                for s in students_in_course:
                    new_take = Take(email=s.email, AID=new_assignment.AID, submitTime=None, grade=None)
                    db.session.add(new_take)
                # commit db change
                db.session.commit()
                # send user to assignment page
                return redirect(url_for('assignments.assignments'))
            # if file is not allowed
            else:
                flash('File extension is not allowed!')
                return render_template('create-assignment.html', form=form)

    # if request method is GET or form not valid re-render create assignment page
    return render_template('create-assignment.html', form=form)


# Student view of assignment
# Author: Jiayuan Zhang
@assignments_blueprint.route('/assignments/content', methods=('GET', 'POST'))
@login_required
@requires_roles('student')
def assignments_content():
    # get assignment
    if request.method == 'POST':
        assignment_id = request.form.get('assignmentID')
        assignment = Assignment.query.filter_by(AID=assignment_id).first()
    # get take
    take = Take.query.filter_by(email=current_user.email, AID=assignment_id).first()

    return render_template('assignment-content.html', assignment=assignment, take=take)


# Download assignment file
# Author: Jiayuan Zhang
@assignments_blueprint.route('/assignment/download')
@login_required
@requires_roles('student')
def download():
    return 0