const fs = require('fs');
const mysql = require('mysql2/promise');
const { Parser } = require('json2csv');
const { exec } = require('child_process');
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

    const filePath = '/Users/matthewlindsey/Desktop/Backend/data-exports/geocode_results.csv';
    fs.writeFileSync(filePath, csv);
    console.log('✅ CSV file updated in /data-exports');

    await connection.end();

    // Auto commit to GitHub
    exec(
      `cd /Users/matthewlindsey/Desktop/Backend && git add ${filePath} && git commit -m "Auto-update CSV export" && git push`,
      (error, stdout, stderr) => {
        if (error) {
          console.error('Git push error:', error);
        } else {
          console.log('CSV file committed & pushed to GitHub');
        }
      }
    );
  } catch (err) {
    console.error('Error exporting CSV:', err);
  }
}

module.exports = exportCSV;
