#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource
from directory import Directory
import asyncio, json

app = Flask(__name__)
api = Api(app)

# Initialise and update the directory to get information about sensors on the network
# (e.g. info such as id, ip_address, status)
directory = Directory()
directory.update()

# Classes for handling HTTP requests
class Home(Resource):
    def get(self):
        return directory.get_dict()

class Test(Resource):
    def get(self):
        list_of_test = [{'test' : '0'}, {'test' : '1'}, {'test' : '2'}]
        return {'list of test' : list_of_test}

class SensorQuery(Resource):

    asyncio_event_loop = asyncio.get_event_loop()

    def get(self, device_id, sensor_chip, measurement):

        sensor = directory.get_list_of_sensors()[device_id]
        
        # NOTE: run this flask server with the option "threaded=False" to prevent
        # asyncio errors such as "event loop is already running" 

        resource = self.asyncio_event_loop.run_until_complete(
            sensor.get_resource(sensor_chip, measurement))

        return resource

class Clustering(Resource):

    def get(self):
        json_file = open("./clustering.json", "rt")
        json_string = json_file.read()
        json_file.close()

        return json.loads(json_string)

# Start Data Recorder        
# import data_recorder
# sensors = directory.get_list_of_sensors()
# data_recorder.start(sensors)

# Initialising the HTTP REST API server
api.add_resource(Home, '/')
api.add_resource(Test, '/test')
api.add_resource(SensorQuery, '/<int:device_id>/<string:sensor_chip>/<string:measurement>')
api.add_resource(Clustering, '/analytics/clustering')
app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)