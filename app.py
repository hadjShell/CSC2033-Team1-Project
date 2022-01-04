from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import sshtunnel
import socket

"""
This python file handles the launching of the application as well as connecting to the database via an SSH tunnel.
-------------------------------------------------------------------------------------------------------------------
Created by Harry Sayer, Jiayuan Zhang
"""

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

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


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html')


# REGISTER PAGE VIEW
@app.route('/register')
def register():
    return render_template('register.html')


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
