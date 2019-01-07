#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource
from directory import Directory, SensorTag

app = Flask(__name__)
api = Api(app)

# Query the directory to get the list of sensors 
# (which are dictionaries containing info such as id, ip_address, status)
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
    import asyncio
    asyncio_event_loop = asyncio.get_event_loop()

    def get(self, sensor_id, resource):
        print('sensor id = %d' % sensor_id)
        print('resource = %s' % resource)
        sensor = directory.get_list_of_sensors()[sensor_id]

        if (resource == 'temperature'):
            value = self.asyncio_event_loop.run_until_complete(sensor.get_temperature())
            unit = 'celsius'

        elif (resource == 'humidity'):
            value = self.asyncio_event_loop.run_until_complete(sensor.get_humidity())
            unit = '%RH'

        return {'value' : value, 'unit' : unit}
        

# Initialising the HTTP REST API server
api.add_resource(Home, '/')
api.add_resource(Test, '/test')
api.add_resource(SensorQuery, '/<int:sensor_id>/<string:resource>')
app.run(debug=True, host='10.0.0.3', port=5000)