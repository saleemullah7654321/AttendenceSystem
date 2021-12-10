from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from face_detection import FaceDetectionAndRecognition



def video_feed(request):
	return StreamingHttpResponse(FaceDetectionAndRecognition().generate_frames(),
					content_type='multipart/x-mixed-replace; boundary=frame')
def index(request):
    return render(request, 'index.html')
