const maria = require('mysql')
const conn = maria.createConnection({
  host: 'localhost',
  port: 3306,
  user: 'root',
  password: 'mariapass',
  database: 'raspi_db',
})

module.exports = conn