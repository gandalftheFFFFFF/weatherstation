import json
import socket
import time
from dataclasses import dataclass, field
from datetime import datetime
from requests.exceptions import ConnectionError

try:
    import sensor
except:
    print('Could not import real sensor module. Importing mock instead')
    import mock_sensor as sensor

import requests


@dataclass
class Buffer:
    data: list = field(default_factory=list)

    def add(self, d):
        self.data.append(d)

    def has_data(self):
        return len(self.data) > 0

    def clear(self):
        self.data = []


def get_config():
    return json.load(open('config.json'))


def main():

    config = get_config()

    timestamp_format = '%Y-%m-%dT%H:%M:%S'

    DHT = sensor.DHT()

    buffer = Buffer()

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
        print(f'Attempting to send live data: {data}')
        try:

            # Latest live data:
            requests.post(server_url, data=data)

            # If buffer contains anything, send it to server as well
            if buffer.has_data():
                data_to_send = buffer.data
                buffer_length = len(data_to_send)
                for x, buffer_data in enumerate(data_to_send):
                    print(f'Sending data from buffer ({x + 1}/{buffer_length})')
                    requests.post(url=server_url, data=buffer_data)
                buffer.clear()

        except ConnectionError as ce:
            print(f'Could not connect to server url: {server_url}. Will buffer and send later')
            buffer.add(d=data)

        time.sleep(config.get('data_interval', 900))


if __name__ == '__main__':
    main()


