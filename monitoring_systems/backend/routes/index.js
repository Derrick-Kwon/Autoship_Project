var express = require('express');
var router = express.Router();

const maria = require('../database/connect/maria')
const axios = require('axios')

// import { parse } from 'csv-parse'

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/api/fetch', function (req, res) {
  genData(maria)
  maria.query('select * from sample order by id desc limit 1', (err, rows, fields) => {
    if (!err) res.send(rows)
    else {
      console.log('err: ', err)
      res.send(err)
    }
  })
})

router.get('/api/weather', async function (req, res) {
  const longitude = 127.3604
  const latitude = 36.3721
  try {
    const response = await axios.get(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation_probability,rain,showers,snowfall,weathercode,pressure_msl,surface_pressure,windspeed_10m&daily=weathercode&current_weather=true&timezone=Asia%2FTokyo&forecast_days=1`)

    console.log(response.data)
    res.send(response.data)
  }
  catch (error) {
    console.log(error)
  }
})

function genData(conn) {
  const sql = "INSERT INTO sample(id,create_time,longitude,latitude,progress,\
    communication,`windSpeed`,`windDirection`,temperature,precipitation,`RPM`,\
    fuel,direction,mode,danger,status,speed,crash,tilt) \
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
  const id = 0
  const create_time = new Date()
  const longitude = 180 * Math.random()
  const latitude = 180 * Math.random()
  const progress = 100 * Math.random()
  const communication = Math.floor(3 * Math.random()) + 1
  const windSpeed = 100 * Math.random()
  const windDirection = 360 * Math.random()
  const temperature = 40 * Math.random()
  const precipitation = 60 * Math.random()
  const RPM = 500 + 500 * Math.random()
  const fuel = 100 * Math.random()
  const direction = 360 * Math.random()
  const mode = 'autonomous'
  const danger = 100 * Math.random()
  const status = 'safe'
  const speed = 30 + 70 * Math.random()
  const crash = 100 * Math.random()
  const tilt = 30 * Math.random()
  const values = [id, create_time, longitude, latitude, progress, communication, windSpeed, windDirection, temperature, precipitation, RPM, fuel, direction, mode, danger, status, speed, crash, tilt]
  conn.query(sql, values, (err, rows, fields) => {
    if (err) console.log(err)
    else console.log('data generated', rows)
  })
}

module.exports = router;
