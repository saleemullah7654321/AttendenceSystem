import cv2
import face_recognition
from app1.models import register
from mark_attendence import MarkAttendence
import os
from datetime import datetime
import time


class FaceDetectionAndRecognition:
    _instance = None

    def __init__(self):
        self.attendence = MarkAttendence()
        self.all_users = register.objects.all()
        self.encodings = list(map(lambda x: x.base64_to_numpy, self.all_users))
        # print(len(self.all_users))
        # print(len(self.encodings))
        self.camera = False
        self.count = 20
        self.face_cascade = cv2.CascadeClassifier(
            "./model/haarcascade_frontalface_default.xml"
        )

    # singleton
    def __new__(self):
        if not self._instance:
            self._instance = super(FaceDetectionAndRecognition, self).__new__(self)
        return self._instance

    # use for making required directories
    def mk_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    # destructor
    def __del__(self):
        self.release_camera()

    # open camera for streaming
    def use_camera(self):
        if not self.camera:
            self.cam = cv2.VideoCapture(0)
            self.camera = True
        return self.cam

    # close camera for streaming
    def release_camera(self):
        if self.camera:
            self.cam.release()
            self.camera = False

    # use for generate frame for displaying current image on web view
    def generate_frames(self):
        self.use_camera()
        while True:
            success, frame = self.cam.read()
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            box, detections = self.face_cascade.detectMultiScale2(gray, minNeighbors=8)
            #  this is use for delay between 1st comparison to 2nd comparison
            if self.count < 20:
                self.count += 1
            # send frame for comparison
            if len(detections) > 0 and detections[0] >= 45 and self.count % 20 == 0:
                self.count = 0
                res = self.face_rec(frame)
                cv2.putText(
                    frame,
                    res,
                    ((x + w) // 2, (y + h) // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    [0, 255, 0],
                    2,
                )
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            elif len(detections) > 0 and detections[0] >= 20:
                x, y, w, h = box[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(
                    frame,
                    str(detections[0]),
                    (0, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    [255],
                    2,
                )
            if not success:
                break
            else:
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    # compare list of encodings fetch from db with given frame
    def face_rec(self, frame):
        unknown_encoding = face_recognition.face_encodings(frame)
        if not unknown_encoding:
            return "Unknown"
        unknown_encoding = unknown_encoding[0]
        results = face_recognition.compare_faces(
            self.encodings, unknown_encoding, tolerance=0.55
        )
        if True in results:
            _time = datetime.now().time().strftime("%H:%M:%S")
            date = datetime.now().date().strftime("%Y-%m-%d")
            idx = results.index(True)
            id = self.all_users[idx].emp_id
            name = self.all_users[idx].name
            self.attendence.insert_attendence(id, name, _time, date)
            print(id, name, _time, date)
            return name
        return "Unknown"

