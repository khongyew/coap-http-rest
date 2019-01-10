import asyncio
from aiocoap import Context, Message

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
    
    async def get_temperature(self):
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
            # print('Result: %s %r'%(response_from_server.code, response_from_server.payload))
            return response_from_server.payload.decode('UTF-8')

    async def get_humidity(self):
        #Uses CoAP client to get temperature readings from a sensor tag
        coap_client = await Context.create_client_context()
        my_uri = 'coap://' + '[' + self.ip_address + ']' + '/sen/hdc/h'
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