from flask import Flask, render_template, redirect, request, Response, Blueprint, url_for
import requests
from iotech.models import User
from iotech.wtform_fields import RegistrationForm, LoginForm
from flask_socketio import emit
from io import StringIO, BytesIO
import io
from PIL import Image
import PIL
import cv2
import imutils
import numpy as np
import base64
from iotech import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from iotech.extensions import db, bcrypt, socketio
from flask_login import login_user, current_user, logout_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html', form=None)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=password, email=form.email.data)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            return redirect(url_for('main.dashboard'))
        else:
            form.password.errors.append('incorrect password')

    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
    
classifier =load_model(r'iotech/static/assets/hand_gesture.h5')
labels = ['Five', 'Four', 'One', 'Three', 'Two']

@socketio.on("disconnect")
def socket_disconnect():
    print("disconnect")

@socketio.on('image')
def image(data):
    sbuf = StringIO()
    sbuf.write(data)
    b = io.BytesIO(base64.b64decode(data))
    pimg = Image.open(b)
    frame = cv2.cvtColor(cv2.flip(np.array(pimg), 1), cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (50,50), (306,306), (0, 255, 255), 2)

    roi_rect = frame[50:306, 50:306]

    gray = cv2.cvtColor(roi_rect, cv2.COLOR_BGR2GRAY)
    _, thresh_binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    roi_64 = cv2.resize(thresh_binary, (64, 64), interpolation=cv2.INTER_AREA)

    # IMAGE PREPROCESSING
    if np.sum([roi_64]) != 0:
        roi = roi_64.astype('float') / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        # PREDICTION
        prediction = classifier.predict(roi)[0]
        label = labels[prediction.argmax()]

        cv2.putText(frame, label, (330,330), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(frame, 'Accuracy - '+str(max(prediction)*100)[0:6], (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    else:
        cv2.putText(frame, 'No Hands Detected', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # requests.get("http://192.168.1.10/"+label)
    # requests.get("http://")
    imgencode = cv2.imencode('.png', frame)[1]
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/png;base64,'
    stringData = b64_src + stringData
    emit('response_back', stringData)