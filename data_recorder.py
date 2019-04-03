# get readings every 5 mins using directory

from directory import Directory
import asyncio
import datetime, threading, time
import os, csv

loop = asyncio.get_event_loop() # TODO: Make the loop non-global

# Readings to get:
# light             10.0.0.3:5000/0/opt/light
# temperature       10.0.0.3:5000/0/tmp/amb
#                   10.0.0.3:5000/0/hdc/t
# humidty           10.0.0.3:5000/0/hdc/h

# Gets the readings from the Sensor Tag
# Returns light, temperature, humidity as a tuple 
def get_all_readings(sensors=None, sensor_id=None, sensor_instance=None):

    # Code will be running in a newly spawned thread, outside of the main thread 
    # asyncio.get_event_loop() will fail in the new thread
    # See this: https://stackoverflow.com/questions/50935153/runtimeerror-there-is-no-current-event-loop-in-thread-dummy-1
    #  
    # asyncio.new_event_loop() will create some other issues
    # Best solution for now: make the event loop from the main thread available as a global variable

    if sensors is not None and sensor_id is not None:
        sensor = sensors[sensor_id]

    elif sensor_instance is not None:
        sensor = sensor_instance
    
    else:
        print('error') 

    # fut = asyncio.gather(
    #     sensor.get_resource('opt', 'light'),
    #     sensor.get_resource('tmp', 'amb'),
    #     sensor.get_resource('hdc', 'h')
    # )

    # ret = loop.run_until_complete(fut)

    # light           = ret[0]['value']
    # temperature     = ret[1]['value']
    # humidity         = ret[2]['value']

    light = loop.run_until_complete(sensor.get_resource('opt', 'light'))['value']
    temperature = loop.run_until_complete(sensor.get_resource('tmp', 'amb'))['value']
    humidity = loop.run_until_complete(sensor.get_resource('hdc', 'h'))['value']

    return light, temperature, humidity

def periodic_record(filename, sensors, period, start_time=time.time()):
    # Using threading.Timer() without drift:
    # https://stackoverflow.com/a/18180189

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
    timestamp = datetime.datetime.now().replace(microsecond=0) # Date Time without microseconds
    timestamp = str(timestamp)

    csvfile = open(filename , 'a', newline='')
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
        data = [timestamp, id, light, temperature, humidity]
        writer.writerow(data)
        print(data)
    
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
    # Generate a new filename every time the recorder is started (or restarted)
    # Sensor reading will be written (appended) to that file (with the filename)

    filename = generate_filename()
    print('writing to ' + filename)
    periodic_record(filename, sensors, 60)

if __name__ == "__main__":
    directory = Directory()
    directory.update()

    sensors = directory.get_list_of_sensors()

    start(sensors)
