from flask import Flask, jsonify, render_template
from gps import *

app = Flask(__name__)
cgps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

@app.route('/')
def index():
    return render_template('1029_point_cloud.html')  

@app.route('/get_position')
def get_position():
    nx = cgps.next()
    if nx['class'] == 'TPV':
        latitude = getattr(nx, 'lat', None)
        longitude = getattr(nx, 'lon', None)
        return jsonify(latitude=latitude, longitude=longitude)
    else:
        return jsonify(error="No GPS data available")

if __name__ == '__main__':
      app.run(debug=True)