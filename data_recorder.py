# get readings every 5 mins using directory

from directory import Directory
import asyncio
import datetime, threading, time
import os, csv


# Readings to get:
# light             10.0.0.3:5000/0/opt/light
# temperature       10.0.0.3:5000/0/tmp/amb
#                   10.0.0.3:5000/0/hdc/t
# humidty           10.0.0.3:5000/0/hdc/h

# Gets the readings from the Sensor Tag
# Returns light, temperature, humidity as a tuple 
def get_all_readings(sensors=None, sensor_id=None, sensor_instance=None):
    # loop = asyncio.get_event_loop()

    # Code will be running outside of the main thread
    # New asyncio event loop needs to be created 
    # https://stackoverflow.com/questions/50935153/runtimeerror-there-is-no-current-event-loop-in-thread-dummy-1

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if sensors is not None and sensor_id is not None:
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

def periodic_record(filename, sensors, period, start_time=time.time()):
    next_time = start_time + period
    
    # Do processing here
    # ------------------- 

    # print(datetime.datetime.now())

    record_readings(filename, sensors)

    # ------------------
    # End of processing 

    interval = next_time - time.time()

    t = threading.Timer(
        interval, 
        periodic_record, 
        args=[filename, sensors, period], 
        kwargs={'start_time':next_time}
    )

    t.start()

def record_readings(filename, sensors):
    timestamp = datetime.datetime.now()

    csvfile = open(filename , 'a')
    writer = csv.writer(csvfile)

    # Write CSV column headings if the file is empty (i.e new file)
    if (os.stat(filename).st_size == 0):
        writer.writerow(['timestamp', 'id', 'light', 'temperature', 'humidity'])

    for sensor in sensors:

        # Read the 3 readings for each sensor
        light, temperature, humidity = get_all_readings(sensor_instance = sensor)

        # Get Sensor ID
        id = sensor.id

        # Write to CSV file
        writer.writerow([timestamp, id, light, temperature, humidity])
    
    csvfile.close()

# Generate filename that does not yet exist in the directory
# Example:  if "sensor-data-0.csv" is already in the dir, 
#           the method will return "sensor-data-1.csv"
# The file name has a increasing index 
def generate_filename():
    index = 0
    while os.path.exists('sensor-data-%s.csv' % index):
        index += 1

    filename = 'sensor-data-%s.csv' % index
    return filename

def test():
    # Write to CSV file
    # incremental file names
    filename = generate_filename()
    
    directory = Directory()
    directory.update()

    sensors = directory.get_list_of_sensors()

    # for i in range(len(sensors)):
    #     light, temperature, humidity = get_all_readings(sensor_id = i)
    #     print(light, temperature, humidity)

    record_readings(filename, sensors)

def start(sensors):
    filename = generate_filename()
    periodic_record(filename, sensors, 10)

if __name__ == "__main__":
    directory = Directory()
    directory.update()

    sensors = directory.get_list_of_sensors()

    start(sensors)
