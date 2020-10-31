import time
import requests
import socket

from datetime import datetime


def read_dht():
    # placeholder
    return 20, 65


def read_bmp280():
    # placeholder
    return 997


while True:

    timestamp_format = '%Y-%m-%dT%H:%M:%S'
    timestamp = datetime.now().strftime(timestamp_format)
    temperature, humidity = read_dht()

    pressure = read_bmp280()

    hostname = socket.gethostname()

    data = {
        'hostname': hostname,
        'timestamp': timestamp,
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
    }

    server_url = 'http://127.0.0.1:5000/data'

    requests.post(server_url, data=data)

    time.sleep(10)