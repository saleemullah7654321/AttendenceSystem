from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from face_detection import FaceDetectionAndRecognition
from mark_attendence import MarkAttendence
from datetime import datetime

attendanceObj = MarkAttendence()
face_rec = FaceDetectionAndRecognition()


def video_feed(request):
    return StreamingHttpResponse(
        face_rec.generate_frames(),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


def index(request):
    global face_rec
    del face_rec
    face_rec = FaceDetectionAndRecognition()
    return render(request, "index.html")


def attendance(request):
    face_rec.release_camera()
    # date=datetime.now().date().strftime("%Y-%m-%d")
    # all_users=list(attendanceObj.dbData.attendancesystems.app1_attendance.find({"Date":date},{'_id':0}))
    all_users = list(
        attendanceObj.dbData.attendancesystems.app1_attendance.find({}, {"_id": 0})
    )
    context = {
        "person": all_users,
        # 'date': date
    }
    return render(request, "attendance.html", context)
