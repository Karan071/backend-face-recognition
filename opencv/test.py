from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
# 
from datetime import datetime, time

video = cv2.VideoCapture(0)
face_detect = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
faces_data = []

with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)

with open('data/faces_data.pkl', 'rb') as f:
     FACES = pickle.load(f)


KNN = KNeighborsClassifier(n_neighbors=5)
KNN.fit(FACES, LABELS)

COL_NAMES = ["Name","Time"]

while True:
    ret, attendance_frame = video.read()
    grey_scale = cv2.cvtColor(attendance_frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(grey_scale, 1.3, 2)
    for (x, y, w, h) in faces:
        cropped_img = attendance_frame[y: y + h, x: x + w : ]
        resized_img = cv2.resize(cropped_img, (50, 50)).flatten().reshape(1,-1)
        output = KNN.predict(resized_img)

        ts = time.time()
        record_date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        record_time = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

        cv2.rectangle(attendance_frame, (x,y), (x+w, y+h), (0,0,255),1)
        cv2.rectangle(attendance_frame, (x,y), (x+w, y+h), (50,50,255),1)
        cv2.rectangle(attendance_frame, (x,y-40), (x+w, y), (50,50,255),-1)

        attendance = [str(output[0]), str(record_time)]

        cv2.putText(attendance_frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255),2)
        cv2.rectangle(attendance_frame, (x, y), (x + w, y + h), (50, 50, 255), 3)
    cv2.imshow('frame', attendance_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

