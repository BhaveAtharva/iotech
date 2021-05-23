from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")
bcrypt = Bcrypt()
bootstrap = Bootstrap()
db=SQLAlchemy()