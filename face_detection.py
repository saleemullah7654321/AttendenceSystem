import cv2
import face_recognition
from mark_attendence import MarkAttendence
import os
import glob
from datetime import datetime
from deepface import DeepFace
import pymongo
from pymongo import MongoClient
from pymongo import collection


class FaceDetectionAndRecognition:
    def __init__(self):
        self.attendence = MarkAttendence()
        self.dbData = pymongo.MongoClient(
            "mongodb+srv://talat:mongo@test.wupry.mongodb.net/attendancesystems?retryWrites=true&w=majority")
        self.camera = False
        self.mk_dir('images')
        self.mk_dir('testing_images')
        self.face_cascade = cv2.CascadeClassifier(
            './model/haarcascade_frontalface_default.xml')

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
            cv2.waitKey(41)
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            box, detections = self.face_cascade.detectMultiScale2(
                gray, minNeighbors=8)
            if len(detections) > 0 and detections[0] >= 40:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
                res = self.face_rec(frame)
                if res:
                    cv2.putText(frame, 'marked', ((x+w)//2, (y+h)//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 255, 0], 2)
                else:
                    cv2.putText(frame, 'face not found', ((x+w)//2, (y+h)//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, [0, 0, 255], 2)
            elif len(detections) > 0 and detections[0] >= 20:
                x, y, w, h = box[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
                cv2.putText(frame, str(
                    detections[0]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, [255], 2)
            # cv2.imshow('',frame)
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def face_rec(self, frame):
        # store best frame as temp image
        unknown_path = f'./testing_images/1.jpg'
        cv2.imwrite(unknown_path, frame)

        unknown_image = face_recognition.load_image_file(unknown_path)
        if not face_recognition.face_encodings(unknown_image):
            return False
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        # list all images in our local folder set from admin form
        for i in os.listdir('images'):
            img_path = f"images/{i}"
            known_image = face_recognition.load_image_file(img_path)
            if not face_recognition.face_encodings(known_image):
                continue
            biden_encoding = face_recognition.face_encodings(known_image)[0]
            results = face_recognition.compare_faces(
                [biden_encoding], unknown_encoding, tolerance=0.5)
            
            # if face matched
            if results[0] == True:
                time = datetime.now().time().strftime("%H:%M:%S")
                date = datetime.now().date().strftime("%d/%m/%Y")
                data = list(self.dbData.attendancesystems.app1_register.find(
                    {'image': f'images/{i}'}))
                # check if this image path exist in db
                if data:
                    id = data[0]['emp_id']
                    name = data[0]['name']
                    self.attendence.insert_attendence(id, name, time, date)
                    print(id, name, time, date)
                    return True
                break
        return False


# dbData = pymongo.MongoClient("mongodb+srv://talat:mongo@test.wupry.mongodb.net/attendancesystems?retryWrites=true&w=majority")
# data=list(dbData.attendancesystems.app1_register.find({ 'image':f'images/saleem.jpg'  }))
# print(data[0]['emp_id'])
