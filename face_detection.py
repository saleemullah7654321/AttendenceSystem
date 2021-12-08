import time
import cv2
import face_recognition
from mark_attendence import MarkAttendence
import os
import datetime


attendence=MarkAttendence()
class FaceDetectionAndRecognition:
    def __init__(self):
        self.camera = False
        self.mk_dir('static/images')
        self.mk_dir('static/testing_images')
        self.camera = False
        self.face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')



    def mk_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def use_camera(self):
        if not self.camera:
            self.cam = cv2.VideoCapture(0)
            self.camera = True
        return self.cam

    def __del__(self):
        self.release_camera()

    def release_camera(self):
        if self.camera:
            self.cam.release()
            self.camera = False

    def generate_frames(self):
        self.use_camera()
        while True:
            success, frame = self.cam.read()

            cv2.waitKey(41)
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            box,detections = self.face_cascade.detectMultiScale2(gray,minNeighbors=8)
            if len(detections)>0 and detections[0]>=50:
                self.face_rec(frame)
                x,y,w,h=box[0]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    def face_rec(self,frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        known_img = face_recognition.load_image_file(frame)
        known_img_encoding = face_recognition.face_encodings(known_img)[0]

        for i in os.listdir('./static/images'):
            img_path=f'./static/images/{i}'
            unknown_img = face_recognition.load_image_file(img_path)
            unknown_img_encoding = face_recognition.face_encodings(unknown_img)[0]            
            results = face_recognition.compare_faces([known_img_encoding], unknown_img_encoding,tolerance=0.5)
            if results[0]:
                time=datetime.now().time().strftime("%H:%M:%S")
                date=datetime.now().date().strftime("%d/%m/%Y")
                attendence.insert_attendence(i.split('.')[0],time,date)



FaceDetectionAndRecognition().generate_frames()