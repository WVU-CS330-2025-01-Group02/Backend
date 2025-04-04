require('dotenv').config();
const axios = require('axios');

const NOAA_TOKEN = process.env.NOAA_API_TOKEN;
const BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2';

// Fixed version using object literal (no 'this' binding issues)
module.exports = {
  async getWeatherByLocation(lat, lng) {
    // Local function avoids 'this' problems
    const getFIPSCode = (lat, lng) => '36'; // NY FIPS (mock)
    
    try {
      const response = await axios.get(`${BASE_URL}/data`, {
        headers: { 'token': NOAA_TOKEN },
        params: {
          datasetid: 'GHCND',
          locationid: `FIPS:${getFIPSCode(lat, lng)}`, // Fixed call
          limit: 1
        }
      });
      
      // Formatting function
      const formatData = (raw) => raw.results.map(item => ({
        date: item.date,
        value: item.value,
        type: item.datatype
      }));
      
      return formatData(response.data);
      
    } catch (error) {
      throw new Error(`NOAA request failed: ${error.message}`);
    }
  }
};