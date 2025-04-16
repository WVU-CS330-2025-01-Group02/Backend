# UPDATE 4/15

# TO DO

~~1. upload walkability index~~

~~2. upload gazetter place file~~

~~3. run and see the current workings of pulling from the datasets~~

~~4. fix any bugs~~

5. verify that it works properly and grabs the correct data and is works for majority of cities (CURRENT STEP: GRAB SPESIFIC DATA)

6. if time: try to get it on front end, sorting function, compare mode

# ! NOTES !

## FEATURES
- converts gazetter file from txt to csv
- reads and merges location database with walkability data
- calculates geographic centroids from block group shapefiles
- matches user input city names to coordinates
- finds the nearest block group using spatial distance
- returns the row from the walkability data associated with the city

## GETTING STARTED

### DATA SOURCE
- [U.S. Census Gazetteer Files (2024)](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html)
- [EPA Smart Location Database](https://www.epa.gov/smartgrowth/smart-location-mapping#SLD)
- [TIGER/Line Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)

### PREREQUISITES
- python
- pandas
- numpy
- geopandas
- shapely
- scipy
- requests

install using
```bash
pip install -r requirements.txt
```

make sure you have the following datasets in the project directory
- 2024_Gaz_place_national.txt
- EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv
- cb_2022_us_bg_500k/

run in terminal
```bash
python datasets.py
```

try city lookups by editing datasets.py and adding at the end for example
```python
get_walkability_from_place("Los Angeles")
get_walkability_from_place("Morgantown")
get_walkability_from_place("Marietta")
```

example output
```bash
Matched input 'los angeles' to gazetteer name 'East Los Angeles CDP'
=======================================================================
nearest block group to 'los angeles' is 780109701002
walkability data -         OBJECTID       GEOID10       GEOID20  STATEFP  ...  GEOID_12digit         GEOID           LAT           LON
220706    220707  7.801100e+11  7.801100e+11       78  ...   780109701002  780109701002  2.008181e+06 -7.193518e+06
```