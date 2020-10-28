from bson import ObjectId
from bson.errors import InvalidId
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
        return format_return_message("Success", "students", output)

    def get_student(self, student_id):
        log.info('Getting Student With Id ' + student_id)
        try:
            response = self.collection.find_one({"_id": ObjectId(student_id)})
            if response:
                return format_return_message("Success", "student", get_student_obj(response))
            else:
                return format_return_message("Failed", "message", "Student Not Found")
        except InvalidId:
            return format_return_message("Failed", "message", "Invalid Object Id")

    def create_student(self, data):
        log.info('Creating Student')
        response = self.collection.insert_one(data)
        return_obj = self.collection.find_one({"_id": ObjectId(response.inserted_id)})
        return format_return_message("Success", "student", get_student_obj(return_obj))

    def update_student(self, student_id, data):
        log.info('Updating Student With Id ' + student_id)
        try:
            response = self.collection.find_one_and_update({"_id": ObjectId(student_id)}, {'$set': data})
            if response:
                return format_return_message("Success", "student", get_student_obj(response))
            else:
                return format_return_message("Failed", "message", "Student Not Found")
        except InvalidId:
            return format_return_message("Failed", "message", "Invalid Object Id")

    def delete_student(self, student_id):
        log.info('Deleting Student With Id' + student_id)
        try:
            response = self.collection.find_one_and_delete({"_id": ObjectId(student_id)})
            if response:
                return format_return_message("Success", "student", get_student_obj(response))
            else:
                return format_return_message("Failed", "message", "Student Not Found")
        except InvalidId:
            return format_return_message("Failed", "message", "Invalid Object Id")


def get_student_obj(response):
    output = {}
    for data in response:
        if data == '_id':
            output[data] = str(response[data])
        else:
            output[data] = response[data]
    return output


def format_return_message(status, key, response):
    output = {
        "Status": status,
        key: response
    }
    return output
