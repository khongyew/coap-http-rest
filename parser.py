# this module is designed to parse the HTML homepage of the Border Router (the gateway for the 6LoWPAN sensor network)
# the purpose is to find the IP Address of the sensors available on the network
# Sample HTML homepage of the Border Router: 
'''
<html>
  <head>
    <title>Contiki-NG</title>
  </head>
<body>
  Neighbors
  <ul>
    <li>fe80::212:4b00:b01:7a86</li>
    <li>fe80::212:4b00:b00:9202</li>
  </ul>
  Routing links
  <ul>
    <li>fd00::212:4b00:b01:7a86 (parent: fd00::212:4b00:812:4) 540s</li>
    <li>fd00::212:4b00:b00:9202 (parent: fd00::212:4b00:812:4) 720s</li>
  </ul>
</body>
</html>

'''

from html.parser import HTMLParser

class BorderRouterHtmlParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.routing_links_title_found = False
        self.ul_starttag_found = False
        self.li_starttag_found = False

        self.sensor_ip_addr = []
        

    def handle_starttag(self, tag, attrs):

        if (self.routing_links_title_found and tag == 'ul'):
            # print("neighbour title found")
            self.ul_starttag_found = True
        
        elif (self.ul_starttag_found and tag == 'li'):
            self.li_starttag_found = True

        # print("Encountered a start tag:", tag)

    def handle_data(self, data):
        data = data.strip()

        if (data == 'Routing links'):
            self.routing_links_title_found = True

        elif (self.li_starttag_found):
            ip_addr = data.split(' ')[0]
            self.sensor_ip_addr.append(ip_addr)

        # print("Encountered some data  :", data)
    
    def handle_endtag(self, tag):
        if (self.ul_starttag_found and tag == 'ul'):
            self.ul_starttag_found = False

        if (self.li_starttag_found and tag == 'li'):
            self.li_starttag_found = False

        # print("Encountered a end tag  :", tag)

    def get_sensor_ip_addr(self):
        return self.sensor_ip_addr