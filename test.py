import cv2.data
from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
import win32com.client
from win32com.client import Dispatch

def speak(str1):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(str1)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

with open('E:/Internships/Internship - Zidio(Data Analyst)/face punching/data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('E:/Internships/Internship - Zidio(Data Analyst)/face punching/data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

COL_NAMES = ['NAME', 'TIME']

# Dictionary to store the last time attendance was marked for each person
attendance_tracker = {}

# Time limit (e.g., 60 seconds) to avoid marking attendance frequently for the same person
TIME_LIMIT = 60  # 60 seconds

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        name = str(output[0])

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist = os.path.isfile(f"Attendance/Attendance_{date}.csv")

        # Check if the person has already been marked within the TIME_LIMIT
        if name in attendance_tracker:
            last_marked_time = attendance_tracker[name]
            if ts - last_marked_time < TIME_LIMIT:
                continue  # Skip if the person was marked recently

        # Mark attendance if time limit has passed
        attendance_tracker[name] = ts

        # Draw face rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, name, (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Attendance data
        attendance = [name, str(timestamp)]

        # Writing to CSV
        mode = 'a' if exist else 'w'
        with open(f"Attendance/Attendance_{date}.csv", mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(COL_NAMES)  # Write header only if file is new
            writer.writerow(attendance)

        # Optional: Play a sound or notification when attendance is marked
        speak("Attendance Taken for " + name)

    # Show frame
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)

    # Break condition to exit the loop
    if k == ord('q'):
        break

    #time.sleep(5)  # You can reduce this sleep time to make detection more responsive

# Clean up resources
video.release()
cv2.destroyAllWindows()
