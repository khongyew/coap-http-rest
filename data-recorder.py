# get readings every 5 mins using directory

from directory import Directory
import asyncio
import datetime, threading, time
import os, csv

directory = Directory()
directory.update()

sensors = directory.get_list_of_sensors()

# Readings to get:
# light             10.0.0.3:5000/0/opt/light
# temperature       10.0.0.3:5000/0/tmp/amb
#                   10.0.0.3:5000/0/hdc/t
# humidty           10.0.0.3:5000/0/hdc/h

# Gets the readings from the Sensor Tag
# Returns light, temperature, humidity as a tuple 
def get_all_readings(sensor_id=None, sensor_instance=None):
    # loop = asyncio.get_event_loop()

    # Code will be running outside of the main thread
    # New asyncio event loop needs to be created 
    # https://stackoverflow.com/questions/50935153/runtimeerror-there-is-no-current-event-loop-in-thread-dummy-1

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if sensor_id is not None:
        sensor = sensors[sensor_id]    

    elif sensor_instance is not None:
        sensor = sensor_instance
    
    else:
        print('error') 

    fut = asyncio.gather(
        sensor.get_resource('opt', 'light'),
        sensor.get_resource('tmp', 'amb'),
        sensor.get_resource('hdc', 'h')
    )

    ret = loop.run_until_complete(fut)

    light           = ret[0]['value']
    temperature     = ret[1]['value']
    humidty         = ret[2]['value']

    return light, temperature, humidty

def data_recorder(filename, start_time=time.time()):
    next_time = start_time + 300 # period
    
    # Do processing here
    # ------------------- 

    # print(datetime.datetime.now())

    record(filename)

    # ------------------
    # End of processing 

    interval = next_time - time.time()
    threading.Timer(interval, data_recorder, args=[filename], kwargs={'start_time':next_time}).start()

def record(filename):
    timestamp = datetime.datetime.now()

    csvfile = open(filename , 'a')
    writer = csv.writer(csvfile)

    # CSV column headings
    writer.writerow(['timestamp', 'id', 'light', 'temperature', 'humidity'])

    for sensor in sensors:

        # Read the 3 readings for each sensor
        light, temperature, humidity = get_all_readings(sensor_instance = sensor)

        # Get Sensor ID
        id = sensor.id

        # Write to CSV file
        writer.writerow([timestamp, id, light, temperature, humidity])
    
    csvfile.close()


def test():
    # Write to CSV file
    # incremental file names
    i = 0
    while os.path.exists('sensor-data-%s.csv' % i):
        i += 1

    filename = 'sensor-data-%s.csv' % i

    # for i in range(len(sensors)):
    #     light, temperature, humidity = get_all_readings(sensor_id = i)
    #     print(light, temperature, humidity)

    record(filename)

def test1():
    index = 0
    while os.path.exists('sensor-data-%s.csv' % index):
        index += 1

    filename = 'sensor-data-%s.csv' % index
    data_recorder(filename)

test()

