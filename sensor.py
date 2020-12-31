import Adafruit_DHT


class DHT:
    def __init__(self):
        self.dht_sensor = Adafruit_DHT.DHT22
        self.dht_pin = 4

    def read_dht(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.dht_pin)
        return temperature, humidity

    def read_bmp280(self):
        return 997  # Placeholder

