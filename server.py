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
    query = """select hostname, ts as timestamp, temperature, humidity, pressure from data order by ts asc"""
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
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
    all_data = query_data(conn=db_connection)
    rows = list(map(lambda x: f'{x[0]},{x[1].strftime("%Y-%m-%dT%H:%M:%S")},{x[2]},{x[3]},{x[4]}', all_data))

    print(list(rows))
    return '<br/>'.join(rows)
    #return render_template('index.html', temperature_list=temperature_list, timestamp_list=timestamp_list, humidity_list=humidity_list)


@app.route('/data', methods=['POST'])
def data():
    form = request.form
    hostname = form['hostname']
    timestamp = form['timestamp']
    temperature = float(form['temperature'])
    humidity = float(form['humidity'])
    pressure = float(form['pressure'])

    insert_query = """insert into data 
                      (hostname, ts, temperature, humidity, pressure) 
                      values (%s, %s, %s, %s, %s)"""

    try:
        cursor = db_connection.cursor()
        cursor.execute(insert_query, (hostname, timestamp, temperature, humidity, pressure))
    except Exception as e:
        print(f'Something went wrong :(')
        print(f'Args: {",".join([hostname, timestamp, temperature, humidity, pressure])}')
        db_connection.rollback()
        print(e)
    else:
        db_connection.commit()
    finally:
        cursor.close()

    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

