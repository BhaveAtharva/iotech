import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

cap = cv2.VideoCapture(0)
classifier =load_model(r'C:\Users\asifa\PycharmProjects\Hand Gesture Recognition Model\hand_gesture.h5')
labels = ['Five', 'Four', 'One', 'Three', 'Two']

while True:
    _, frame = cap.read()
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

    cv2.imshow('image', frame)
    cv2.imshow('thresh', thresh_binary)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
