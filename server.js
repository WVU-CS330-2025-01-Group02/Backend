require('dotenv').config();
const express = require('express');
const cors = require('cors');
const weatherRoutes = require('./weatherRoutes');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api', weatherRoutes);

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`NOAA Backend running on http://localhost:${PORT}`);
});