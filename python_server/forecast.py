from datetime import datetime, timedelta
import grid
import requests

base = datetime.now() - timedelta(minutes=30)

year = str(base.year)
month = str(base.month)
day = str(base.day)

dateString = year + month + day
hours = str(base.hour)
minutes = str(base.minute)
seconds = str(base.second)

metric_of = {
  'T1H': '℃',
	'RN1':	'mm',
	'UUU':	'm/s',
	'VVV':	'm/s',
	'REH':	'%',
	'PTY': '',
	'VEC':	'deg',
	'WSD':	'm/s',
}

description_of = {
  'T1H': 'temperature',
	'RN1':	'precipitation per 1 hour',
	'UUU':	'east-west wind composition',
	'VVV':	'south-north wind composition',
	'REH':	'humidity',
	'PTY':  'precipitation form',
	'VEC':	'wind direction',
	'WSD':	'wind speed',
}

# Convert forecast response into proper format
def convert_forecast(response):
  response_body = response.json()["response"]["body"]
  itemlist = response_body["items"]["item"]
  result = {}

  for item in itemlist:
    result[item['category']] = {
      'value': item['obsrValue'],
      'metric': metric_of[item['category']],
      'decription': description_of[item['category']],
    }

  return result

# Get base time for forecasting
def base_time():
  if base.minute < 30:
    return str(base.hour) + "00"
  else:
    return str(base.hour) + "30"


# Forecast
def api_forecast(lat, lng):
  # 여기서 위도경도를 좌표로 바꿔주도록 한다
  position = grid.dfs_xy_conv("toXY", lat, lng)
  print(position)
  url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
  params = {
    "serviceKey": "KnqHi2dIa1Z5DikYH66mNjQ31mQlH0bCyzPuaRUtyfJaQErYUwfuyH/vaGJT4719UQQYFBP8gyj1iS1KDPs4FA==",
    "pageNo": 1,
    "numOfRows": 60,                  # 10개의 카테고리에서 6개씩 나옴
    "dataType": 'json',
    "base_date": dateString,
    "base_time": base_time(),  # 변환된 시간
    "nx": position["x"],
    "ny": position["y"],
  }
  print("params: ", params)
  response = requests.get(url, params)
  # print("response: ", response.json())
  result = convert_forecast(response)
  return result


if __name__ == '__main__':
  # test code
  api_forecast(36.3721, 127.3604)