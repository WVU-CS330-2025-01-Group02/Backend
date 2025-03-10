const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());



// Database configuration
require('dotenv').config();

const dbConfig = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT
};

// Create database connection pool
const pool = mysql.createPool(dbConfig);

// Test endpoint
app.get('/api/data', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM your_table');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database error' });
  }
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Create new user
app.post('/api/users', async (req, res) => {
    try {
      const { name, email } = req.body;
      const [result] = await pool.query(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        [name, email]
      );
      res.status(201).json({ id: result.insertId });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Database error' });
    }
  });
  
  // Get user by ID
  app.get('/api/users/:id', async (req, res) => {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM users WHERE id = ?',
        [req.params.id]
      );
      res.json(rows[0] || {});
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Database error' });
    }
  });

  // Get location by GEOID
app.get('/api/locations/:geoid', async (req, res) => {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM epa_smart_location WHERE GEOID = ?',
        [req.params.geoid]
      );
      res.json(rows[0] || null);
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Database error' });
    }
  });
  
  // Search locations with pagination
  app.get('/api/locations', async (req, res) => {
    try {
      const page = parseInt(req.query.page) || 1;
      const limit = parseInt(req.query.limit) || 100;
      const offset = (page - 1) * limit;
  
      const [rows] = await pool.query(
        'SELECT * FROM epa_smart_location LIMIT ? OFFSET ?',
        [limit, offset]
      );
      
      res.json({
        page,
        limit,
        results: rows
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Database error' });
    }
  });