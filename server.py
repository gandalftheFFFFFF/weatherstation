from flask import Flask
from flask import request, render_template

app = Flask(__name__)


def split_helper(line):
    s = line.split('\t')
    hostname = s[0]
    timestamp = s[1]
    temperature = s[2]
    humidity = s[3]
    pressure = s[4]
    return hostname, timestamp, temperature, humidity, pressure


@app.route('/')
def index():
    # load file contents
    with open('data.tsv', 'r') as f:
        data = f.read()
        lines = data.splitlines()
        hostname_list = []
        timestamp_list = []
        temperature_list = []
        humidity_list = []
        pressure_list = []

        for line in lines:
            hostname, timestamp, temperature, humidity, pressure = split_helper(line)
            timestamp_list.append(timestamp)
            temperature_list.append(temperature)

        return render_template('index.html', temperature_list=temperature_list, timestamp_list=timestamp_list)


@app.route('/data', methods=['POST'])
def data():
    form = request.form
    hostname = form['hostname']
    timestamp = form['timestamp']
    temperature = form['temperature']
    humidity = form['humidity']
    pressure = form['pressure']

    data_string = '\t'.join([hostname, timestamp, temperature, humidity, pressure])

    with open('data.tsv', 'a+') as f:
        f.write(f'{data_string}\n')

    return 'ok'


app.run('0.0.0.0', debug=True)

