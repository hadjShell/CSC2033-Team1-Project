import logging
import socket
import os
from functools import wraps
from flask import Flask, render_template, request, current_app
from flask_login import LoginManager, current_user
from flask_login.config import EXEMPT_METHODS
from flask_sqlalchemy import SQLAlchemy

"""
This python file handles the launching of the application as well as connecting to the database via an SSH tunnel.
-------------------------------------------------------------------------------------------------------------------
Created by Harry Sayer, Jiayuan Zhang
"""

# CONFIG
UPLOAD_FOLDER = '/static/teachers_submission'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LOCAL DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///odin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""
tunnel = sshtunnel.SSHTunnelForwarder('linux.cs.ncl.ac.uk', ssh_username='',
                                      ssh_password='',
                                      remote_bind_address=('cs-db.ncl.ac.uk', 3306))
tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://csc2033_team01:SonsArchVeer@127.0.0.1:{}/csc2033_team01'.format(
    tunnel.local_bind_port)
"""

# Initial the db
db = SQLAlchemy(app)


# Security logging
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return "SECURITY" in record.getMessage()


filehandler = logging.FileHandler('Odin.log', 'w')
filehandler.setLevel(logging.WARNING)
filehandler.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s|%(message)s', '%m/%d/%Y|%I:%M:%S %p')
filehandler.setFormatter(formatter)

logger = logging.getLogger('')
logger.propagate = False
logger.addHandler(filehandler)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html')


# REGISTER PAGE VIEW
@app.route('/register')
def register():
    return render_template('register.html')


# ERROR PAGE VIEWS
# Author: Jiayuan Zhang
@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(403)
def page_forbidden(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errors/503.html'), 503


# DECORATORS
# custom login _required decorator
# Author: Jiayuan Zhang
def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            # log anonymous users invalid attempts
            logging.warning('SECURITY - Anonymous invalid access| | |%s', request.remote_addr)
            # Redirect the user to an unauthorised notice!
            return current_app.login_manager.unauthorized() and render_template('errors/403.html')
        return func(*args, **kwargs)

    return decorated_view


# Role access control
# Author: Harry Sayer
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # anonymous user has no role, nothing done
            if not current_user.is_authenticated:
                return f(*args, **kwargs)
            elif current_user.role not in roles:
                # security log when a user attempts to access a page they don't have the required permissions to
                logging.warning('SECURITY - UNAUTHORISED ACCESS ATTEMPT|%s|%s|%s',
                                current_user.UID,
                                current_user.email,
                                request.remote_addr)
                # Redirect user to error page
                return render_template('errors/403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User


    @login_manager.user_loader
    def load_user(email):
        return User.query.get(email)


    # BLUEPRINTS
    # import blueprints
    from users.views import users_blueprint
    from courses.views import courses_blueprint
    from assignments.views import assignments_blueprint
    from administrator.views import administrator_blueprint

    # register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(courses_blueprint)
    app.register_blueprint(assignments_blueprint)
    app.register_blueprint(administrator_blueprint)

    app.run(host=my_host, port=free_port, debug=True)
