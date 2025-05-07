# Backend for Weather We Go ☁️
> Weather We Go is a web application that allows a user to see weather and walkability data for a specific location.

## File Structure 🗂️
```bash
├── .vscode
│   ├── settings.json
├── FMR
│   ├── .gitignore
│   └── fmrService.js
│   └── package.json
├── NOAAadverseweather
│   ├── noaaService.js
│   └── simpleTest.js
├── Walkability
│   ├── city_walkability_data.csv
│   └── datasets.py
├── WeatherWeGo-auth
│   ├── client
│       ├── public
│           ├── favicon.ico
│           └── logo192.png
│           └── logo512.png
│           └── manifest.json
│           └── robots.txt
│       └── src
│           ├── App.css
│           └── App.js
│           └── App.test.js
│           └── Login.js
│           └── index.css
│           └── index.js
│           └── login.html
│           └── logo.svg
│           └── register.html
│           └── reportWebVitals.js
│           └── setupTests.js
│       └── .gitignore
│       └── README.md
│       └── package-lock.json
│       └── package.json
│   └── .gitignore
│   └── Local MySQL.session.sql
│   └── package-lock.json
│   └── package.json
│   └── server.js
├── .gitignore
├── README.md (you are here!)
├── package-lock.json
└── package.json
``` 

## Notable Files
- <code>fmrService.js</code>
  - Fetches 2025 FMR data by FIPS code
  - Data includes fair market rent values by number of bedrooms
- <code>noaaService.js</code>
  - Gets extreme weather event counts from GSOY
  - Matches a location with its nearest GSOY station
  - Extreme weather is defined as days with thunderstorms, over 1" of snowfall, temperature ≥ 90°F, or wind speed ≥ 35 mph
- <code>datasets.py</code>
  - Takes multiples files and merges them to be uploaded to Azure

## Resources Used
- Node.js
- MySQL
- NOAA API
- HUB FMR API
- EPA Smart Location Database
- Python
