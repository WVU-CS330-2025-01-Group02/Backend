const mysql = require('mysql2');
require('dotenv').config();

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

try {
  connection.connect((err) => {
    if (err) {
      console.error('Failed to connect to DB:', err);
      throw err;
    }
    console.log('Connected to MySQL database');
  });
} catch (err) {
  console.error('DB connection error caught:', err);
}

module.exports = connection;
