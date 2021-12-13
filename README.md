
# Attendance System

This project is build on django python framework. In this project, face is recognize 
to mark attendance of employee. which is store in mongo db. we can also see all records
from web view.

## Optimizations

In this Optimizations are done by storing face encodings to mongobd agains all employee
image. Because encodings takes many time to compute result. so we store encoding of image
on the time of registration which produce 100 time better result than making encodins at runtime.

## Installation

make sure python>=3.7 is istalled on your system because it created on 3.7.
visual studio must install. otherwise it will not work for you. from visual studio 
installer install Desktop Development with c++.
Run this commands from any terminal.

```bash
  git clone https://github.com/saleemullah7654321/AttendenceSystem.git
  cd AttendenceSystem
  code . // if vs code is installed on your system. otherwise skip this line
  python -m pip install -r requirements.txt
  python .\manage.py runserver
```
  after this it start execution, This link http://127.0.0.1:8000/  appears. Goto this
  link you will see output.
## 🛠 Skills
python, django, mongodb


## Screenshots

On this Page your face is recognizing for attendence. If exist it marks your attendence
to db.Ensure that, you must change db connection string from 
myproject/settings.py==>DATABASES, and 
for attendance mark_attendence.py ==> self.dbData = pymongo.MongoClient(....)

![Main Page](https://github.com/saleemullah7654321/AttendenceSystem/blob/master/Screenshots/1.PNG?raw=true)

on this Page all records from db shown here!

![Attendence Page](https://github.com/saleemullah7654321/AttendenceSystem/blob/master/Screenshots/2.PNG?raw=true)

when you go for register new person firstime it ask for login, so name is admin and password is admin.
After login go into Registers add or update records. If login in create issue then python manage.py createsuperuser
run this command in terminal. It ask for name and password. you enter your name and desired password.

![registration Page](https://github.com/saleemullah7654321/AttendenceSystem/blob/master/Screenshots/3.PNG?raw=true)


## Authors

- [@Saleem Ullah](https://github.com/saleemullah7654321/AttendenceSystem.git)
- [@Haseeb Khokhar](https://github.com/khokharhaseeb/Tasks)
- [@Talat Ghafoor](https://github.com/saleemullah7654321/AttendenceSystem.git)
- [@Umer Ehsan](https://github.com/saleemullah7654321/AttendenceSystem.git)
