const express = require('express');
const router = express.Router();
const { getWeatherByLocation } = require('./noaaService');

router.get('/weather', async (req, res) => {
  try {
    const { lat, lng } = req.query;
    if (!lat || !lng) throw new Error('Missing coordinates');
    
    const data = await getWeatherByLocation(lat, lng);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;