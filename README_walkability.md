# City Walkability Matching
This project links U.S. place-level data from the U.S. Census Gazetter with block group-level walkability scores from the EPA Smart Location Database. It uses spatial joins to associate each place with its nearest Census block group and retrieves the National Walkability Index for that location

## Project Structure
```graphsql
├── 2024_Gaz_place_national.txt          # U.S. Census place-level Gazetteer data (input)
├── EPA_SmartLocationDatabase_V3_*.csv   # EPA walkability data (input)
├── cb_2022_us_bg_500k/                  # Folder containing Census TIGER shapefiles for block groups
├── datasets.py                          # Main processing script
├── city_walkability_data.csv            # Output file: place-level data with walkability index
└── README_walkability.md                            # You're here!
```

## Features
- Converts raw TXT Gazetter data to CSV for easier handling
- Loads and preprocesses EPA Smart Location Database
- Performs nearest neighbor spatial joins to match cities to the closest block group within 50km
- Merges in the EPA's National Walkability Index for each matched block group
- Outputs a clean CSV file with the results

## How to Run
1. Download required data:
- 2024 Gazetter National Place TXT
- EPA Smart Location Database CSV
- Census Block Group Shapefiles
2. Run the script
```bash
python datasets.py
```
3. Output
- A new file named city_walkability_data.csv will be created containing
    - City name
    - State
    - Nearest block group's GEOID
    - Latitude and Longitude
    - Walkability Index (0-20 scale)
