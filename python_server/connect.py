from datetime import datetime
import math
import random
from flask import jsonify
import mysql.connector
import forecast
import grid

# 데이터베이스 연결을 위한 설정값. 실행하는 환경에 따라 다르게 설정해 준다.
user = "root"
pw = "kwon6821"
db = "mydatabase" #데이터베이스이름"

# conn = mysql.connector.connect(
#   host="localhost",
#   user= user,
#   password= pw ,
#   database=db,
#   autocommit=True,
# )

# cursor = conn.cursor()

def insert_data(values):
  # insert_query = "INSERT INTO sample(id, create_time, longitude, latitude, progress, \
  # communication, windSpeed, windDirection, temperature, precipitation, RPM, \
  # fuel, direction, mode, danger, status, speed, crash, tilt) \
  # VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
  insert_query = "insert into sensor(id, create_time, latitude, longitude, speed, \
    pitch, roll, risk)\
    values(0, %s, %s, %s, %s, %s, %s, %s)"
  conn = mysql.connector.connect(
    host="localhost",
    user= user,
    password= pw ,
    database=db,
    autocommit=True,
  )
  cursor = conn.cursor()
  print(values[0:7])
  cursor.execute(insert_query, (datetime.now(), ) + values[0:6])
  result = cursor.fetchone() 

  ridar_insert = "insert into ridar(id, create_time, angle, distance) \
    values(0, %s, %s, %s)"
  ridar = []
  for i in range(len(values[6])):
    ridar.append((datetime.now(), values[6][i][0], values[6][i][1]))
  # print(ridar)
  cursor.executemany(ridar_insert, ridar)
  cursor.close()
  conn.close()
  return 

def insert_weather(values):
  conn = mysql.connector.connect(
    host="localhost",
    user= user,
    password= pw ,
    database=db,
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
    user= user,
    password= pw ,
    database=db,
    autocommit=True,
  )
  cursor = conn.cursor()

  fetch_message = "select * from sensor order by id desc limit 1;"
  cursor.execute(fetch_message)

  result_row = cursor.fetchone()
  result = {}

  columns = cursor.description
  # Convert result row into an object
  for i in range(len(result_row)):
      result[columns[i][0]] = result_row[i]

  ridar_message = "select * from ridar order by id desc limit 100;"
  cursor.execute(ridar_message)
  result_rows = cursor.fetchall()
  ridars = []
  for i in range(len(result_rows)):
    ridars.append((result_rows[i][2], result_rows[i][3]))
  result['ridar'] = ridars
  print("ridars: ", ridars)

  cursor.close()
  conn.close()
  return jsonify(result)

def get_latest_weather():
  conn = mysql.connector.connect(
    host="localhost",
    user= user,
    password= pw ,
    database=db,
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
    user= user,
    password= pw ,
    database=db,
    autocommit=True,
  )
  cursor = conn.cursor()

  # get latest weather
  result = get_latest_weather()
  
  # if the result is new, request for new data.
  new_position = grid.dfs_xy_conv("toXY", lat, lng)
  # if result == {}:
  #   print("result empty")
  #   return result    
  # else:
  #   if result['basetime'][8:12] != forecast.base_time():
  #     print("different basetime: ", result['basetime'][8:12], "", forecast.base_time())
  #   if result['nx'] != new_position['x'] or result['ny'] != new_position['y']:
  #     print("different position")

  if result != {} and result['basetime'] == forecast.base_time() and result['nx'] == new_position['x'] and result['ny'] == new_position['y']:
    return result

  # Get weather data
  forecast_result = forecast.api_forecast(lat, lng)
  # if forecast_result['basetime'] == result['basetime'] and result['nx'] == new_position['x'] and result['ny'] == new_position['y']:
  #   return result

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
  create_time = datetime.now()
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