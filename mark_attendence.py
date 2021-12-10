import pymongo
from pymongo import MongoClient
from pymongo import collection
class MarkAttendence:
    def __init__(self):
        self.dbData = pymongo.MongoClient("mongodb+srv://talat:mongo@test.wupry.mongodb.net/attendancesystems?retryWrites=true&w=majority")
    def insert_attendence(self,id,name,current_time,current_date):
        if len(list(self.dbData.attendancesystems.app1_attendance.find({"$and":[{"emp_id":id},{"Date":current_date}]}))) != 0:
            return 'Already Mark Attendence'
        else:
            self.dbData.attendancesystems.app1_attendance.insert_one({"emp_id": id, "name": name, "Time": current_time,'Date':current_date,'Status':'Present'})
            return 'Attendence Marked'
    def view_all_data(self):
        return list(self.dbData.attendancesystems.app1_attendance.find({}))
        
    def view_by_date(self,date):
        self.dbData.attendancesystems.app1_attendance.find({"Date":date})