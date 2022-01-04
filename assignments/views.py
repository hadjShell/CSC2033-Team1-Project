from flask import Blueprint, render_template
from sqlalchemy import desc
from flask_login import current_user, login_required
from app import db
from assignments.forms import AssignmentForm
from models import Assignment

# CONFIG
assignments_blueprint = Blueprint('assignments', __name__, template_folder='templates')


# VIEW
# Assignment page view
# Author: Jiayuan Zhang
@assignments_blueprint.route('/assignments')
def assignments():
    # render assignment page
    return render_template('assignment.html')


@assignments_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = AssignmentForm()

    if form.validate_on_submit():
        new_assignnment = Assignment(email=current_user.email, assignmentName=form.assignmentTitle.data,
                                     description=form.assignmentDescription.data, deadline=form.assignmentDeadline.data,
                                     CID=form.assignmentCID.data)
        db.session.add(new_assignnment)
        db.session.commit()

        return assignment()
    return render_template('create.html', form=form)
