from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sshtunnel

"""
This python file handles the launching of the application as well as connecting to the database via an SSH tunnel.
-------------------------------------------------------------------------------------------------------------------
Created by Harry Sayer
"""
app = Flask(__name__)

tunnel = sshtunnel.SSHTunnelForwarder('linux.cs.ncl.ac.uk', ssh_username='uni_username', ssh_password='uni_password',
                                      remote_bind_address=('cs-db.ncl.ac.uk', 3306))
tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://csc2033_team01:SonsArchVeer@127.0.0.1:{}/csc2033_team01'.format(
    tunnel.local_bind_port)

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(email):
        return User.query.get(email)

    app.run()
