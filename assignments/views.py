from flask import Blueprint, render_template
from sqlalchemy import desc
from flask_login import current_user, login_required
from app import db
from assignments.forms import AssignmentForm
from models import Assignment, Create

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


@assignments_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = AssignmentForm()

    if form.validate_on_submit():
        new_assignnment = Assignment(email=current_user.email, assignmentName=form.assignmentTitle.data,
                                     description=form.assignmentDescription.data, deadline=form.assignmentDeadline.data,
                                     CID=form.assignmentCID.data)
        db.session.add(new_assignnment)
        db.session.commit()

        return assignments()
    return render_template('create.html', form=form)
