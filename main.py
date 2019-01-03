#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource
from directory import Directory

app = Flask(__name__)
api = Api(app)

# Classes for handling HTTP requests
class Home(Resource):
    def get(self):
        return {'available sensors' : list_of_sensors}

class Test(Resource):
    def get(self):
        list_of_test = [{'test' : '0'}, {'test' : '1'}, {'test' : '2'}]
        return {'list of test' : list_of_test}

# Query the directory to get the list of sensors 
# (which are dictionaries containing info such as id, ip_address, status)
directory = Directory()
directory.update()
list_of_sensors = directory.get_list_of_sensors()

# Initialising the HTTP REST API server
api.add_resource(Home, '/')
api.add_resource(Test, '/test')
app.run(debug=True, host='10.0.0.3', port=5000)