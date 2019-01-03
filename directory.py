# This module helps to discover the Sensor Tags (the IP addresses) on the 6LoWPAN network
# This module also helps to discover the resources available on the CoAP Server of each Sensor Tags
# The idea is to show the discovered information on the root page of the HTTP REST server

import urllib.request
from parser import BorderRouterHtmlParser
from json import *

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
        pass

    def parse(self):
        html_content = urllib.request.urlopen(self.BORDER_ROUTER_URL).read()
        html_content = html_content.decode('UTF-8')

        html_parser = BorderRouterHtmlParser()
        html_parser.feed(html_content)

        # get the list of sensor tag ip addresses
        list_of_ip_addr = html_parser.get_sensor_ip_addr()

        # build the list of dictionaries of sensor tag
        # for example:
        # list_of_sensors = [{'id': '0', 'ip_address' : 'fd00::212:4b00:b01:7a86'},
        #                    {'id': '1', 'ip_address' : 'fd00::212:4b00:b00:9202'}]
        id = 0
        for ip_address in list_of_ip_addr:
            sensor = SensorTag(id, ip_address)
            self.list_of_sensors.append(sensor.get_dict())
            id = id + 1

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