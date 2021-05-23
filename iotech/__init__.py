from flask import Flask, render_template, redirect, request

from iotech.wtform_fields import *
# from iotech.models import User

import cv2
from .extensions import db, bootstrap, bcrypt, socketio

from .routes.main import main
from .commands import create_tables

# from flask_bootstrap import Bootstrap

def create_app(config_file='settings.py'):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)


    bcrypt.init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    socketio.init_app(app)
    app.register_blueprint(main)
    app.cli.add_command(create_tables)

    return app
