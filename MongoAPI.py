from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging as log

load_dotenv()


class MongoAPI:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        database = os.getenv("database")
        collection = os.getenv("collection")
        cursor = self.client[database]
        self.collection = cursor[collection]

    def get_students(self):
        log.info('Getting All Students')
        response = self.collection.find()
        output = []
        for data in response:
            obj = {}
            for item in data:
                if item == '_id':
                    obj[item] = str(data[item])
                else:
                    obj[item] = data[item]
            output.append(obj)
        return output

    def get_student(self, student_id):
        log.info('Getting Student With Id ' + student_id)
        response = self.collection.find_one({"_id": ObjectId(student_id)})
        output = {}
        if response:
            for data in response:
                if data == '_id':
                    output[data] = str(response[data])
                else:
                    output[data] = response[data]
        else:
            output = {"error": "Student Not Found"}
        return output

    def create_student(self, data):
        log.info('Creating Student')
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Inserted_Id': str(response.inserted_id)}
        return output

    def update_student(self, student_id, data):
        log.info('Updating Student')
        response = self.collection.update_one({"_id": ObjectId(student_id)}, {'$set': data})
        if response.modified_count == 0:
            return {'Status': 'Nothing was updated'}
        else:
            return {'Status': 'Successfully Updated'}

    def delete_student(self, student_id):
        log.info('Deleting Student')
        response = self.collection.delete_one({"_id": ObjectId(student_id)})
        if response.deleted_count == 0:
            return {'Status': 'Student not found'}
        else:
            return {'Status': 'Successfully Deleted'}
