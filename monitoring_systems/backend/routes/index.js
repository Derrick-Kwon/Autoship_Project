var express = require('express');
var router = express.Router();

const maria = require('../database/connect/maria')


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
