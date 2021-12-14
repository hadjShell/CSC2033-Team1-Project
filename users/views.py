from flask import Blueprint, render_template, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from models import User
from users.forms import LoginForm

users_blueprint = Blueprint('users', name, template_folder='templates')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (form.password == user.password):
            login_user(user)