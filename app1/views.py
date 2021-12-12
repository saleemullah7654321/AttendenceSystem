import json
from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from app1.models import register
from face_detection import FaceDetectionAndRecognition
from django.core import serializers
from mark_attendence import MarkAttendence

attendanceObj=MarkAttendence()
face_rec=FaceDetectionAndRecognition()

def video_feed(request):
	return StreamingHttpResponse(face_rec.generate_frames(),
					content_type='multipart/x-mixed-replace; boundary=frame')
def index(request):
    return render(request, 'index.html')

def attendance(request):
	face_rec.release_camera()
	all_users=list(attendanceObj.dbData.attendancesystems.app1_attendance.find({},{'_id':0}))
	context= {
        'person': all_users
        }
	return render(request,'attendance.html',context)


def test(request):
	face_rec.release_camera()
	all_users=register.objects.all()
	encodings=list(map(lambda x: x.base64_to_numpy,all_users))
	tmpJson = serializers.serialize("json",all_users)
	tmpObj = json.loads(tmpJson)
	return HttpResponse(json.dumps(tmpObj))