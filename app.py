from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import sshtunnel
import socket

"""
This python file handles the launching of the application as well as connecting to the database via an SSH tunnel.
-------------------------------------------------------------------------------------------------------------------
Created by Harry Sayer
"""
app = Flask(__name__)

tunnel = sshtunnel.SSHTunnelForwarder('linux.cs.ncl.ac.uk', ssh_username='username',
                                      ssh_password='password',
                                      remote_bind_address=('cs-db.ncl.ac.uk', 3306))
tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://csc2033_team01:SonsArchVeer@127.0.0.1:{}/csc2033_team01'.format(
    tunnel.local_bind_port)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == 'main':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(email):
        return User.query.get(email)

    from users.views import users_blueprint

    app.register_blueprint(users_blueprint)

    app.run(host=my_host, port=free_port, debug=True)