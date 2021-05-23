from flask import Flask, render_template, redirect, request
from .models import User
import cv2
from .extensions import db, bootstrap, bcrypt, socketio, login_manager
from .routes.main import main
from .commands import create_tables

def create_app(config_file='settings.py'):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)


    bcrypt.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    bootstrap.init_app(app)
    socketio.init_app(app)
    app.register_blueprint(main)
    app.cli.add_command(create_tables)

    return app
