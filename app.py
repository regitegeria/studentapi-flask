from flask import Flask, request, json, Response
from dotenv import load_dotenv
from MongoAPI import MongoAPI

app = Flask(__name__)

load_dotenv()


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/api/students', methods=['GET'])
def get_students():
    mongo = MongoAPI()
    response = mongo.get_students()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/api/student/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def student_information(student_id):
    mongo = MongoAPI()
    response = {}

    if request.method == 'GET':
        response = mongo.get_student(student_id)
    elif request.method == 'PUT':
        data = request.json
        if data is None or data == {}:
            return Response(response=json.dumps({"Error": "Please provide information"}),
                            status=400,
                            mimetype='application/json')
        response = mongo.update_student(student_id, data)
    elif request.method == 'DELETE':
        response = mongo.delete_student(student_id)

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/api/student', methods=['POST'])
def create_student():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    mongo = MongoAPI()
    response = mongo.create_student(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
