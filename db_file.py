import pymongo
from pymongo import MongoClient
from pymongo import collection



class DataBaseCls:
    def __init__(self) -> None:
        dbData = pymongo.MongoClient("mongodb+srv://talat:mongo@test.wupry.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        dbData.myFirstDatabase.employees.insert_one({"_id": 1, "name": "saleem", "Designation": "python"})
    
    
    def insert_data(self,id,name,email,image_path):
        pass

DataBaseCls()