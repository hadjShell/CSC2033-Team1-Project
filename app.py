from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sshtunnel

app = Flask(__name__)

tunnel = sshtunnel.SSHTunnelForwarder('linux.cs.ncl.ac.uk', ssh_username='UniUsername', ssh_password='UniPassword',
                                      remote_bind_address=('cs-db.ncl.ac.uk', 3306))
tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://csc2033_team01:SonsArchVeer@127.0.0.1:{}/csc2033_team01'.format(
    tunnel.local_bind_port)

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
