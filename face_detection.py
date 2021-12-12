import cv2
import face_recognition
from app1.models import register
from mark_attendence import MarkAttendence
import os
from datetime import datetime
import pymongo
import time
from IPython.core.display import display, HTML

class FaceDetectionAndRecognition:
    _instance=None
    def __init__(self):
        self.attendence = MarkAttendence()
        self.all_users=register.objects.all()
        self.encodings=list(map(lambda x: x.base64_to_numpy,self.all_users))
        self.camera = False
        self.count=0
        self.face_cascade = cv2.CascadeClassifier(
            './model/haarcascade_frontalface_default.xml')
    #singleton
    def __new__(self):
        if not self._instance:
            self._instance=super(FaceDetectionAndRecognition,self).__new__(self)
        return self._instance

    def mk_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def use_camera(self):
        if not self.camera:
            self.cam = cv2.VideoCapture(0)
            self.camera = True
        return self.cam

    def release_camera(self):
        if self.camera:
            self.cam.release()
            self.camera = False

    def generate_frames(self):
        self.use_camera()
        while True:
            success, frame = self.cam.read()
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            box, detections = self.face_cascade.detectMultiScale2(
                gray, minNeighbors=8)
            if self.count<20:
                self.count+=1
            if len(detections) > 0 and detections[0] >= 60 and self.count%20==0:
                self.count=0
                res = self.face_rec(frame)
                if res:
                    cv2.putText(frame, 'MARKED', ((x+w)//2, (y+h)//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0], 2)
                    # display(HTML('<script>alert("hello")</script>'))
                    # time.sleep(1)
                else:
                    cv2.putText(frame, 'UNKNOWN', ((x+w)//2, (y+h)//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0, 255], 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            elif len(detections) > 0 and detections[0] >= 20:
                x, y, w, h = box[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.putText(frame, str(
                    detections[0]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, [255], 2)
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def face_rec(self, frame):
        unknown_encoding = face_recognition.face_encodings(frame)
        if not unknown_encoding:
            return False
        unknown_encoding = unknown_encoding[0]
        results = face_recognition.compare_faces(
            self.encodings, unknown_encoding, tolerance=0.5)
        if True in results:
            _time = datetime.now().time().strftime("%H:%M:%S")
            date = datetime.now().date().strftime("%d/%m/%Y")
            idx=results.index(True)
            id = self.all_users[idx].emp_id
            name = self.all_users[idx].name
            self.attendence.insert_attendence(id, name, _time, date)
            print(id, name, _time, date)
            return True
        return False


# dbData = pymongo.MongoClient("mongodb+srv://talat:mongo@test.wupry.mongodb.net/attendancesystems?retryWrites=true&w=majority")
# data=list(dbData.attendancesystems.app1_register.find({'emp_id':4},{'emp_id':1,'image_encoding':1}))[0]
# print(data)
# img=face_recognition.load_image_file('./images/saleem.jpg')
# img_enc=face_recognition.face_encodings(img)
# face_recognition.compare_faces([str(img_enc)],data['image_encoding'])

