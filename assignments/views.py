from flask import Blueprint, render_template, request
from sqlalchemy import desc
from flask_login import current_user
from app import db, login_required, requires_roles
from assignments.forms import AssignmentForm
from models import Assignment, Create, Take, User

# CONFIG
assignments_blueprint = Blueprint('assignments', __name__, template_folder='templates')


# HELP FUNCTIONS
# A function that returns the 'deadline' value
def deadlineValue(a):
    return a.deadline


# VIEW
# Assignment page view
# Author: Jiayuan Zhang
@assignments_blueprint.route('/assignments')
@login_required
@requires_roles('teacher', 'student')
def assignments():
    # get all assignments belonging to current user
    if current_user.role == "teacher":
        assignments = []
        create = Create.query.filter_by(email=current_user.email).all()
        for c in create:
            assignments.append(Assignment.query.filter_by(AID=c.AID).first())
    # TODO: student part

    # sort assignments by deadline
    assignments.sort(key=deadlineValue)

    # render assignment page
    return render_template('assignment.html', assignments=assignments)


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
# Author: Tom Dawson
@assignments_blueprint.route('/create-assignment', methods=['POST', 'GET'])
def create_assignment():
    form = AssignmentForm

    if form.validate_on_submit():
        new_assignment = Assignment(assignmentName=form.assignmentTitle.data,
                                    description=form.assignmentDescription.data, deadline=form.assignmentDeadline.data, CID=form.assignmentCID.data)
        db.session.add(new_assignment)
        db.session.commit()

    return render_template('assignment.html', form=form)
