import datetime
import math
import random
from flask import jsonify
import mysql.connector
import forecast
import grid

# conn = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="mariapass",
#   database="raspi_db",
#   autocommit=True,
# )

# cursor = conn.cursor()

def insert_data(values):
  # insert_query = "INSERT INTO sample(id, create_time, longitude, latitude, progress, \
  # communication, windSpeed, windDirection, temperature, precipitation, RPM, \
  # fuel, direction, mode, danger, status, speed, crash, tilt) \
  # VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
  insert_query = "insert into sensor(id, create_time, latitude, longitude, speed, \
    pitch, roll, risk, angle, distance)\
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kwon6821",
    database="Tables",
    autocommit=True,
  )
  cursor = conn.cursor()
  cursor.execute(insert_query, values)
  result = cursor.fetchone()
  cursor.close()
  conn.close()
  return result

def insert_weather(values):
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kwon6821",
    database="Tables",
    autocommit=True,
  )
  cursor = conn.cursor()

  insert_query = "INSERT INTO weather(id, basetime, nx, ny, T1H, RN1, UUU, VVV, REH, PTY, VEC, WSD) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
  
  cursor.execute(insert_query, values)
  result = cursor.fetchone()
  cursor.close()
  conn.close()
  return result

def get_data():
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kwon6821",
    database="Tables",
    autocommit=True,
  )
  cursor = conn.cursor()

  fetch_message = "select * from sensor order by id desc limit 1;"
  cursor.execute(fetch_message)

  result_row = cursor.fetchone()
  result = {}

  columns = cursor.description
  cursor.close()
  conn.close()

  # Convert result row into an object
  for i in range(len(result_row)):
      result[columns[i][0]] = result_row[i]
  return jsonify(result)

def get_latest_weather():
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kwon6821",
    database="Tables",
    autocommit=True,
  )
  cursor = conn.cursor()

  fetch_message = "select * from weather order by id desc limit 1;"
  cursor.execute(fetch_message)

  result_row = cursor.fetchone()
  result = {}
  columns = cursor.description

  # Convert result row into an object
  if result_row:
    for i in range(len(columns)):
      result[columns[i][0]] = result_row[i]
  cursor.close()
  conn.close()
  return result

def get_weather(lat, lng):
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kwon6821",
    database="Tables",
    autocommit=True,
  )
  cursor = conn.cursor()

  # get latest weather
  result = get_latest_weather()
  
  # if the result is new, request for new data.
  new_position = grid.dfs_xy_conv("toXY", lat, lng)
  if result == {}:
    print("result empty")
  else:
    if result['basetime'][8:12] != forecast.base_time():
      print("different basetime: ", result['basetime'][8:12], "", forecast.base_time())
    if result['nx'] != new_position['x'] or result['ny'] != new_position['y']:
      print("different position")

  if result != {} and result['basetime'] == forecast.base_time() and result['nx'] == new_position['x'] and result['ny'] == new_position['y']:
    return result

  # Get weather data
  forecast_result = forecast.api_forecast(lat, lng)
  if forecast_result['basetime'] == result['basetime'] and result['nx'] == new_position['x'] and result['ny'] == new_position['y']:
    return result

  # Insert weather data into database
  basetime = forecast_result['basetime']
  T1H = forecast_result['T1H']['value']
  RN1 = forecast_result['RN1']['value']
  UUU = forecast_result['UUU']['value']
  VVV = forecast_result['VVV']['value']
  REH = forecast_result['REH']['value']
  PTY = forecast_result['PTY']['value']
  VEC = forecast_result['VEC']['value']
  WSD = forecast_result['WSD']['value']
  nx = forecast_result['nx']
  ny = forecast_result['ny']
  
  weather_row = (0, basetime, nx, ny, T1H, RN1, UUU, VVV, REH, PTY, VEC, WSD)
  insert_weather(weather_row)
  result = get_latest_weather()
  print("latest_row: ", result)
  
  cursor.close()
  conn.close()
  return result
  

def gen_random_data():
  id = 0
  create_time = datetime.datetime.now()
  longitude = 180 * random.random()
  latitude = 180 * random.random()
  progress = 100 * random.random()
  communication = math.floor(3 * random.random()) + 1
  windSpeed = 100 * random.random()
  windDirection = 360 * random.random()
  temperature = 40 * random.random()
  precipitation = 60 * random.random()
  rpm = 500 + 500 * random.random()
  fuel = 100 * random.random()
  direction = 360 * random.random()
  mode = 'autonomous'
  danger = 100 * random.random()
  status = 'safe'
  speed = 30 + 70 * random.random()
  crash = 100 * random.random()
  tilt = 30 * random.random()
  values = (id, create_time, longitude, latitude, progress, communication, windSpeed, windDirection, temperature, precipitation, rpm, fuel, direction, mode, danger, status, speed, crash, tilt)
  
  return insert_data(values)

if __name__ == '__main__':
  # test code
  result = get_weather(36.3721, 127.3604)