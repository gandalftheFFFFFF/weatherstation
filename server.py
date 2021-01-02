from flask import Flask
import psycopg2
import json
from flask import request, render_template


# Get config
config = json.load(open('config.json'))


def connect_db(config):
    hostname = config['db_hostname']
    database = config['db_database']
    username = config['db_username']
    password = config['db_password']
    db_conn = psycopg2.connect(host=hostname, database=database, user=username, password=password)
    print(f'Connected to database: {database}@{hostname}')
    return db_conn


db_connection = connect_db(config)
app = Flask(__name__)


def query_data(conn):
    query = """select hostname, ts as timestamp, temperature, humidity, pressure from data order by ts desc"""
    cursor = conn.cursor()
    result = cursor.execute(query).fetchall()
    return result


def split_helper(line):
    s = line.split('\t')
    hostname = s[0]
    timestamp = s[1]
    temperature = s[2]
    humidity = s[3]
    pressure = s[4]
    return hostname, timestamp, temperature, humidity, pressure  # TODO: Try *s


@app.route('/')
def index():
    all_data = query_data(conn=con)
    return render_template('index.html', temperature_list=temperature_list, timestamp_list=timestamp_list, humidity_list=humidity_list)


@app.route('/data', methods=['POST'])
def data():
    form = request.form
    hostname = form['hostname']
    timestamp = form['timestamp']
    temperature = form['temperature']
    humidity = form['humidity']
    pressure = form['pressure']

    insert_query = """insert into data 
                      (hostname, ts, temperature, humidity, pressure) 
                      values (%s, %s, %s, %s, %s)"""

    cursor = db_connection.cursor()
    cursor.execute(insert_query, (hostname, timestamp, temperature, humidity, pressure))
    db_connection.commit()
    cursor.close()

    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

