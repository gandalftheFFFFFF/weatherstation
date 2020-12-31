import json
import socket
import time
from datetime import datetime

try:
    import sensor
except:
    print('Could not import real sensor module. Importing mock instead')
    import mock_sensor as sensor

import requests


def get_config():
    return json.load(open('config.json'))


def main():

    config = get_config()

    timestamp_format = '%Y-%m-%dT%H:%M:%S'

    DHT = sensor.DHT()

    while True:
        timestamp = datetime.now().strftime(timestamp_format)
        temperature, humidity = DHT.read_dht()

        pressure = DHT.read_bmp280()

        hostname = socket.gethostname()

        data = {
            'hostname': hostname,
            'timestamp': timestamp,
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
        }

        server_url = config['server_url']

        # Attempt to send data to server
        print(f'Sending data: {data}')
        requests.post(server_url, data=data)

        time.sleep(900)


if __name__ == '__main__':
    main()


