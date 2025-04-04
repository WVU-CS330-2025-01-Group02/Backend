const { getWeatherByLocation } = require('./noaaService');

// Test inputs
const testLocation = {
  lat: 40.71,  // NYC latitude
  lng: -74.01   // NYC longitude
};

// Run test
(async () => {
  console.log('=== Running Simple Test ===');
  console.log(`Input Coordinates: ${testLocation.lat}, ${testLocation.lng}`);
  
  try {
    const weatherData = await getWeatherByLocation(
      testLocation.lat,
      testLocation.lng
    );
    
    console.log('\n✅ Test Passed - Got Weather Data:');
    console.log(weatherData);
    
    // Quick validation
    if (!weatherData || !Array.isArray(weatherData)) {
      throw new Error('No weather data returned');
    }
    console.log(`\nReceived ${weatherData.length} data points`);
    
  } catch (error) {
    console.log('\n❌ Test Failed:');
    console.error(error.message);
  }
})();