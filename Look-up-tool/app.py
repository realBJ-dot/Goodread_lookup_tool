from werkzeug.wrappers import response
from utility import  if_id_exist
from database import connect, insert_authors, insert_books
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_from_directory
from bson.json_util import dumps
import json

app = Flask(__name__)
def handle_post(request, is_author):
    data = json.loads(request.data)
    if data:
        if is_author:
            insert_authors(data)
            msg = {"message": "successfully post"}
            json_data = dumps(msg, indent=2)
            response = jsonify(json_data)
            return response
        else:
            insert_books(data)
            msg = {"message": "successfully post"}
            json_data = dumps(msg, indent=2)
            response = jsonify(json_data)
            return response

@app.route('/book', methods=['GET', 'POST', 'DELETE', 'PUT'])
#this function is responsible for api operation on book
def process():
    for i in request.args.keys():
        if i != 'id':
            response = jsonify({"Message" : "Request not supported"})
            response.status_code = 400
            return response
    id = request.args.get('id', None)
    if id != None:
        client = connect()
        db = client['goodreads']
        collations = db['book']
        ##first to check if the id user gave exist in the database
        if if_id_exist(client, id, False) != False:
            ####get
            if request.method == "GET":
                data = if_id_exist(client, id, False)
                response = jsonify(data) 
                return response
            ####delete
            elif request.method == "DELETE":
                data = if_id_exist(client, id, False)
                response = jsonify(data)
                dict = {"book id" : id}
                print(dict)
                collations.delete_one(dict)  
                return response
        else:
            msg = {"Error message" : "Oh no, there is no such id here"}
            data = dumps(msg, indent=2)
            response = jsonify(data)
            return response
    else:
        if request.method == "POST":
            return handle_post(request, True)


    


@app.route('/author', methods=['GET', 'POST', 'DELETE', 'PUT'])
#this function is responsible for api operation on author
def process1():
    for i in request.args.keys():
        if i != 'id':
            response = jsonify({"Message" : "Request not supported"})
            response.status_code = 400
            return response
    id = request.args.get('id', None)
    if id != None:
        client = connect()
        db = client['goodreads']
        collations = db['authors']
        ##first to check if the id user gave exist in the database
        if if_id_exist(client, id, True) != False:
            ##get verb
            if request.method == "GET":
                data = if_id_exist(client, id, True)
                response = jsonify(data)
            ##delete verb
            if request.method == "DELETE":
                data = if_id_exist(client, id, True)
                response = jsonify(data)
                dict = {"author id" : int(id)}
                print(dict)
                collations.delete_one(dict)
                return response
        else:
            msg = {"Error message" : "Oh no, there is no such id here"}
            data = dumps(msg, indent=2)
            response = jsonify(data)
            return response
    else:
        if request.method == "POST":
            return handle_post(request, False)
    

@app.route('/<path:path>')
def server(path):
    return send_from_directory('web', path)
@app.route('/vis/top-authors')
def top_author_visualization():
    return send_from_directory('web', 'AuthorTop.html')

@app.route('/vis/top-books')
def top_book_visualization():
    return send_from_directory('web', 'BookTop.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)