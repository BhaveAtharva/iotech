from flask import Flask, render_template, redirect, request, Response, Blueprint
from iotech.models import User
from iotech.wtform_fields import RegistrationForm, LoginForm
# from iotech import app, db, bcrypt, socketio

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

main = Blueprint('main', __name__)
# @app.route('/')
# @app.route('/base')
# def hello():
#     return render_template('base.html')

@main.route('/')
def home():
    return render_template('home.html', form=None)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    print(type(form))
    print(form)
    if form.validate_on_submit() and not User.query.filter_by(username=form.username.data).first():  
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(bcrypt.check_password_hash(password, form.confirm_password.data))
        print(len(password))
        user = User(username=form.username.data, password=password)
        db.session.add(user)
        db.session.commit()
        return "success"
    if User.query.filter_by(username=form.username.data).first():
        form.username.errors.append('username already taken')
    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            return "loggedin"

    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    return render_template('hand.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    


@main.route('/babecam')
def babecam():
    return render_template('bebcam.html')

# @socketio.on('image')
# def image(data):
    
#     mp_drawing = mp.solutions.drawing_utils
#     mp_hands = mp.solutions.hands
#     hands = mp_hands.Hands(
#         min_detection_confidence=0.5, min_tracking_confidence=0.5)
#     sbuf = StringIO()
#     sbuf.write(data)
    
#     # decode and convert into image
#     b = io.BytesIO(base64.b64decode(data))
#     pimg = Image.open(b)
    
#     frame = cv2.cvtColor(cv2.flip(np.array(pimg), 1), cv2.COLOR_BGR2RGB)

#     # pimg = np.asarray(PIL.Image.open(b))
#     # print(type(pimg))
#     # exit()
#     # converting RGB to BGR, as opencv standards
#     # pimg = cv2.cvtColor(np.float64(pimg), cv2.COLOR_BGR2RGB)

#     frame.flags.writeable = False
#     results = hands.process(frame)

#     frame.flags.writeable = True
#     # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(
#             frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#     # ret, buffer = cv2.imencode('.jpg', pimg)
#     # pimg = cv2.flip(pimg, 1)

#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     imgencode = cv2.imencode('.png', frame)[1]

    
#     # pimg = PIL.Image.fromarray(np.uint8(pimg))
#     # base64 encode
#     stringData = base64.b64encode(imgencode).decode('utf-8')
#     b64_src = 'data:image/png;base64,'
   
   
   
#     stringData = b64_src + stringData



#     # frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

#     #  Process the image frame
#     # frame = imutils.resize(frame, width=700)
#     # frame = cv2.flip(frame, 1)
#     # imgencode = cv2.imencode('.png', frame)[1]
#     # base64 encode
#     # stringData = base64.b64encode(imgencode).decode('utf-8')
#     # b64_src = 'data:image/png;base64,'
#     # stringData = b64_src + stringData

#     # emit the frame back
#     emit('response_back', stringData)
#     # emit('response_back', stringData)

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

    imgencode = cv2.imencode('.png', frame)[1]
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/png;base64,'
    stringData = b64_src + stringData
    emit('response_back', stringData)