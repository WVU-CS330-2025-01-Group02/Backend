const fs = require('fs');
const mysql = require('mysql2/promise');
const { Parser } = require('json2csv');
require('dotenv').config();

async function exportCSV() {
  try {
    const connection = await mysql.createConnection({
      host: process.env.DB_HOST,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
    });

    const [rows] = await connection.execute('SELECT * FROM geocode_results');
    const parser = new Parser();
    const csv = parser.parse(rows);

    const exportDir = './data-exports';
    if (!fs.existsSync(exportDir)) {
      fs.mkdirSync(exportDir);
    }

    fs.writeFileSync(`${exportDir}/geocode_results.csv`, csv);
    console.log('✅ CSV file updated in /data-exports');

    await connection.end();
  } catch (err) {
    console.error('❌ Error exporting CSV:', err);
  }
}

module.exports = exportCSV;
