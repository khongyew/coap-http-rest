# This module is designed to serve as an abstraction of the SensorTag device.
# The user should be able to get sensor readings from the SensorTag device using this module.
# This module uses the CoAP protocol to send request (GET, PUT, DELETE etc.) 
# to the CoAP Server running on the SensorTag device.

from aiocoap import Context, Message, Code

class SensorTag:
    
    coap_client = None
    
    @classmethod
    async def init_coap_client(cls):
        cls.coap_client = await Context.create_client_context()

    @classmethod
    async def make_coap_request(cls, request):
        
        # Create a coap_client instance for the SensorTag class
        # There should only be one coap_client instance that will be used by every SensorTag instance
        # Not wise to generate multiple coap_client instance since it can lead to "too many open files" error
        # https://stackoverflow.com/questions/50951632/oserror-errno-24-too-many-open-files-with-sockets-from-aiocoap-context-req
        if cls.coap_client == None:
            await cls.init_coap_client()
        
        try:
            response_from_server = await cls.coap_client.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            # code = response_from_server.code
            payload = response_from_server.payload.decode('UTF-8')
            return payload

    def __init__(self, id, ip_address):
        self.id = id
        self.ip_address = ip_address    # string
        self.status = 'Available'       # Place holder TODO: implement status

    # Returns a dictionary representation of the SensorTag instance
    # This should contain useful information about the sensor tag 
    def get_dict(self):
        json_dict = {
            'id' : self.id, 
            'ip_address' : self.ip_address,
            'status': self.status
            }
        return json_dict
    
    # Deprecated. Don't use.
    async def get_temperature(self):
        #Uses CoAP client to get temperature readings from a sensor tag
        coap_client = await Context.create_client_context()
        my_uri = 'coap://' + '[' + self.ip_address + ']' + '/sen/tmp/amb'
        # 'coap://[fd00::212:4b00:b01:7a86]/sen/tmp/amb'
        my_request = Message(code=Code.GET, uri=my_uri)

        try:
            response_from_server = await coap_client.request(my_request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            # print('Result: %s %r'%(response_from_server.code, response_from_server.payload))
            return response_from_server.payload.decode('UTF-8')

    # Deprecated. Don't use.
    async def get_humidity(self):
        #Uses CoAP client to get temperature readings from a sensor tag
        coap_client = await Context.create_client_context()
        my_uri = 'coap://' + '[' + self.ip_address + ']' + '/sen/hdc/h'
        # 'coap://[fd00::212:4b00:b01:7a86]/sen/tmp/amb'
        my_request = Message(code=Code.GET, uri=my_uri)

        try:
            response_from_server = await coap_client.request(my_request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            # print('Result: %s\n%r'%(response.code, response.payload))
            return response_from_server.payload.decode('UTF-8')

    # Return resource (sensor readings) in dict/json format
    async def get_resource(self, sensor_chip, measurement):
        my_uri = self.generate_uri(sensor_chip, measurement)

        # print('uri = ' + my_uri)
 
        if(sensor_chip == 'mpu'):
            # MPU sensor query (acc or gyro)
            # need to query readings in x, y and z axis

            x_axis_request = Message(code=Code.GET, uri=(my_uri + '/x'))
            y_axis_request = Message(code=Code.GET, uri=(my_uri + '/y'))
            z_axis_request = Message(code=Code.GET, uri=(my_uri + '/z'))

            ret = {}
            ret['x'] = await self.make_coap_request(x_axis_request)
            ret['y'] = await self.make_coap_request(y_axis_request)
            ret['z'] = await self.make_coap_request(z_axis_request)

            return ret

        else:
            # Regular sensor query
            my_request = Message(code=Code.GET, uri=my_uri)
            value = await self.make_coap_request(my_request)
            return {'value' : value, 'unit' : ''}

    # Generates the uri that will be used to query the CoAP server on the SensorTag 
    def generate_uri(self, sensor_chip, measurement):
        protocol = 'coap://'
        ip_address = '[' + self.ip_address + ']'
        directory = '/sen/' + sensor_chip + '/' + measurement
        
        my_uri = protocol + ip_address + directory

        return my_uri
