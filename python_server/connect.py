import datetime
import math
import random
import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mariapass",
  database="raspi_db",
)

cursor = conn.cursor()

def insert_data(values):
  insert_query = "INSERT INTO sample(id, create_time, longitude, latitude, progress, \
  communication, windSpeed, windDirection, temperature, precipitation, RPM, \
  fuel, direction, mode, danger, status, speed, crash, tilt) \
  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
  
  cursor.execute(insert_query, values)
  result = cursor.fetchone()
  return result


def gen_random_data():
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

