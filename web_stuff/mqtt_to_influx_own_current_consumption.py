
import re
import json
from typing import NamedTuple
 
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
 
INFLUXDB_ADDRESS = '192.168.178.48'
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = '123pax123'
INFLUXDB_DATABASE = 'DBCURRENT' # standard database would b "DBONE"
 
MQTT_ADDRESS = '192.168.178.48'
MQTT_USER = 'admin'
MQTT_PASSWORD = 'pax123'
MQTT_TOPIC = 'delock/+/SENSOR'
MQTT_REGEX = 'delock/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTT_InfluxDB_Bridge'
 
MQTT_FIELDS = [
    'ApparentPower',
    'Current',
    'Voltage',
    'Power',
    'ReactivePower',
    'Factor',
    'Yesterday',
    'Today'

    # hier weitere relevante auflisten
]
 
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
 
class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float
 
def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)
 
def _parse_mqtt_message(topic, payload):
    #print(payload)
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        #return SensorData(location, measurement, float(payload))
        print(payload)
        payload = json.loads(payload)
        for field in MQTT_FIELDS:
            yield SensorData(location, field, float(payload["ENERGY"][field]))
    else:
        return None
 
def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)
 
def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data_sets = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data_sets is None:
        print("Couldn't parse sensor data!")
        return
    for sensor_data in sensor_data_sets:
        _send_sensor_data_to_influxdb(sensor_data)
 
def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)
 
def main():
    _init_influxdb_database()
 
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
 
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()
 
 
if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()