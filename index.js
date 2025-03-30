const express = require('express');
const cors = require('cors');
const db = require('./db');

const app = express();
app.use(cors());
app.use(express.json());

// Save location data from frontend
app.post('/api/save-location', (req, res) => {
  const { user_id, address, latitude, longitude } = req.body;

  const sql = `
    INSERT INTO geocode_results (user_id, address, latitude, longitude)
    VALUES (?, ?, ?, ?)
  `;

  db.query(sql, [user_id, address, latitude, longitude], (err, result) => {
    if (err) {
      console.error('Insert error:', err);
      return res.status(500).json({ error: 'Insert failed' });
    }

    res.status(200).json({ message: 'Location saved', id: result.insertId });
  });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Backend running at http://localhost:${PORT}`);
});

