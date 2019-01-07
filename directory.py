# This module helps to discover the Sensor Tags (the IP addresses) on the 6LoWPAN network
# This module also helps to discover the resources available on the CoAP Server of each Sensor Tags
# The idea is to show the discovered information on the root page of the HTTP REST server

import urllib.request
from parser import BorderRouterHtmlParser
from json import *
import asyncio
from aiocoap import *

# content = urllib.request.urlopen('http://[fd00::212:4b00:812:4]').read()
# content = content.decode('UTF-8')

# parser = BorderRouterHtmlParser()
# parser.feed(content)
# print(content)
# ret = parser.get_sensor_ip_addr()
# print(ret)

class Directory:
    test_string = 'Hello World from Directory'
    BORDER_ROUTER_URL = 'http://[fd00::212:4b00:812:4]'

    def __init__(self):
        self.list_of_sensors = []

    def parse(self):
        html_content = urllib.request.urlopen(self.BORDER_ROUTER_URL).read()
        html_content = html_content.decode('UTF-8')

        html_parser = BorderRouterHtmlParser()
        html_parser.feed(html_content)

        # get the list of sensor tag ip addresses
        list_of_ip_addr = html_parser.get_sensor_ip_addr()

        # build the list of sensor instances
        id = 0
        for ip_address in list_of_ip_addr:
            sensor = SensorTag(id, ip_address)
            self.list_of_sensors.append(sensor)
            id = id + 1

    # returns a dictionary representation of the directory
    def get_dict(self):
        list_of_dict_of_sensors = []

        # build the list of dictionaries of sensor tag
        # for example:
        # list_of_dict_of_sensors = [{'id': '0', 'ip_address' : 'fd00::212:4b00:b01:7a86'},
        #                            {'id': '1', 'ip_address' : 'fd00::212:4b00:b00:9202'}]

        for sensor in self.list_of_sensors:
            list_of_dict_of_sensors.append(sensor.get_dict())
        return {'available sensors' : list_of_dict_of_sensors}

    def update(self):
        self.parse()

    def get_list_of_sensors(self):
        return self.list_of_sensors


class SensorTag:
    def __init__(self, id, ip_address):
        self.id = id
        self.ip_address = ip_address    # string
        self.status = 'Available'       # Place holder TODO: implement status 

    def get_dict(self):
        json_dict = {
            'id' : self.id, 
            'ip_address' : self.ip_address,
            'status': self.status
            }
        return json_dict
    
    async def get_temp(self):
        #Uses CoAP client to get temperature readings from a sensor tag
        coap_client = await Context.create_client_context()
        my_uri = 'coap://' + '[' + self.ip_address + ']' + '/sen/tmp/amb'
        # 'coap://[fd00::212:4b00:b01:7a86]/sen/tmp/amb'
        my_request = Message(code=GET, uri=my_uri)

        try:
            response_from_server = await coap_client.request(my_request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            # print('Result: %s\n%r'%(response.code, response.payload))
            return response_from_server.payload.decode('UTF-8')
