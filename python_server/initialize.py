# 이 코드는 데이터베이스 연결 초기화를 위한 코드입니다.
# connect.py의 10~12번 라인 코드를 실행 환경(db 설정)에 맞게 수정한 후에
# 커맨드 창에 $ python initialize.py 를 치시면 db 초기화가 완료됩니다.
# 이 코드는 기존에 같은 이름의 table이 있다면 제거해버리기 때문에,
# 의도치 않게 데이터를 잃지 않도록 조심해야 합니다.
import mysql.connector
import connect

conn = mysql.connector.connect(
  host="localhost",
  user=connect.user,
  password=connect.pw,
  database=connect.db,
  autocommit=True,
)
cursor = conn.cursor()
init_ridar = "DROP TABLE IF EXISTS ridar;\
  CREATE TABLE `ridar` (\
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',\
    `create_time` datetime DEFAULT NULL COMMENT 'Create Time',\
    `angle` decimal(5,2) DEFAULT NULL,\
    `distance` decimal(6,2) DEFAULT NULL,\
    PRIMARY KEY (`id`)\
  )"
cursor.execute(init_ridar)
cursor.close()
conn.close()

conn = mysql.connector.connect(
  host="localhost",
  user=connect.user,
  password=connect.pw,
  database=connect.db,
  autocommit=True,
)
cursor = conn.cursor()
init_sensor = "DROP TABLE IF EXISTS sensor;\
  CREATE TABLE `sensor` (\
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',\
    `create_time` datetime DEFAULT NULL COMMENT 'Create Time',\
    `latitude` decimal(20,17) DEFAULT NULL,\
    `longitude` decimal(20,17) DEFAULT NULL,\
    `speed` decimal(5,2) DEFAULT NULL,\
    `pitch` decimal(5,2) DEFAULT NULL,\
    `roll` decimal(5,2) DEFAULT NULL,\
    `risk` int(11) DEFAULT NULL,\
    PRIMARY KEY (`id`)\
  )"
cursor.execute(init_sensor)
cursor.close()
conn.close()
