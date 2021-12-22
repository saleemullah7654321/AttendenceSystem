FROM ubuntu


RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.7 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt


RUN python3 -m pip install djongo
RUN python3 -m pip install opencv-python
RUN apt-get update -y && \
    apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y
RUN pip3 install pymongo==3.12.1
RUN pip3 install "pymongo[srv]"
RUN pip3 install pybase64 
RUN apt-get install build-essential cmake pkg-config -y
RUN apt-get install python3-dev -y
RUN pip3 install pickle5
RUN apt-get update -y
RUN pip3 install dlib
RUN pip3 install face_recognition
RUN apt-get install cheese -y
# RUN apt-get install luvcview
# RUN apt-get install guvcview
# RUN apt-get install fswebcam
WORKDIR /app
COPY . /app


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]









# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:slim

# EXPOSE 8000

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# # Install pip requirements
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt


# # RUN  apt-get install python3-pip -y
# RUN python3 -m pip install djongo
# RUN python3 -m pip install opencv-python
# RUN apt-get update -y && \
#     apt-get install build-essential cmake pkg-config -y

# RUN pip install dlib==19.9.0
# RUN python3 -m pip install face-recognition
# RUN python3 -m pip install pymongo==3.12.1
# RUN python3 -m pip install pickle5
# RUN python3 -m pip install pybase64
# RUN python3 -m pip install "pymongo[srv]"
# RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6  -y

# WORKDIR /app
# COPY . /app

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# # File wsgi.py was not found in subfolder: 'AttendenceSystem'. Please enter the Python path to wsgi file.
# # CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythonPath.to.wsgi"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]