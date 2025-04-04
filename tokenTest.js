// testToken.js
require('dotenv').config();
const axios = require('axios');
axios.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets', {
  headers: { token: process.env.NOAA_API_TOKEN }
})
.then(res => console.log('✅ Token valid'))
.catch(err => console.error('❌ Token invalid:', err.response?.data));