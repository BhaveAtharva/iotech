from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from iotech.wtform_fields import *
from flask_bcrypt import Bcrypt
import mediapipe as mp
import cv2
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap

# from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.secret_key = "15e653aeca7896d2adaa414c0f04e17985a136af57dc60c665ed1d6d28d9eed7"
bcrypt = Bcrypt(app)

uri = 'postgres://dgzsajcfmirpue:b5a99a691fb2646cf83ee1082baa909eb70a8528ba726adfc106b5ea852004e4@ec2-54-225-228-142.compute-1.amazonaws.com:5432/d71tc2qd422mm6' # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)
Bootstrap(app)
socketio = SocketIO(app, cors_allowed_origins="*")
from iotech import routes