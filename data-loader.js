const axios = require('axios');
const csv = require('csv-parser');
const { Writable } = require('stream');
const mysql = require('mysql2/promise');
require('dotenv').config();

const CSV_URL = 'https://edg.epa.gov/EPADataCommons/public/OA/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv';

async function loadData() {
  const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_USER,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT
  });

  try {
    const response = await axios.get(CSV_URL, { responseType: 'stream' });
    const parser = csv({
      mapHeaders: ({ header }) => header.trim() // Clean headers
    });

    const inserter = new Writable({
      objectMode: true,
      async write(row, encoding, callback) {
        try {
          await pool.query(
            `INSERT INTO epa_smart_location 
            (GEOID, CSA, CBSA, TotPop, D1A, D1B, D1C, D2A_JPHH, D2B_E8MIXA, D3A, D4A)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP`,
            [
              row.GEOID,
              row.CSA,
              row.CBSA,
              row.TotPop,
              row.D1A,
              row.D1B,
              row.D1C,
              row.D2A_JPHH,
              row.D2B_E8MIXA,
              row.D3A,
              row.D4A
            ]
          );
          callback();
        } catch (err) {
          callback(err);
        }
      }
    });

    response.data
      .pipe(parser)
      .pipe(inserter)
      .on('finish', () => {
        console.log('CSV data successfully loaded');
        pool.end();
      })
      .on('error', (err) => {
        console.error('Error processing CSV:', err);
        pool.end();
      });

  } catch (err) {
    console.error('Error fetching CSV:', err);
  }
}

loadData();