import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mariapass",
  database="raspi_db",
)

cursor = conn.cursor()