# import statements
import pandas as pd
import requests
import time
import re

# convert txt to csv
def txt_to_csv(txt_filepath, csv_filepath):
    try:
        df = pd.read_csv(txt_filepath, sep='\t')
        df.to_csv(csv_filepath, index=False)
        print(f"Successfully converted '{txt_filepath}' to '{csv_filepath}'")
    except FileNotFoundError:
        print(f"Error: File not found: '{txt_filepath}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# file paths
txt_file = 'Backend/2024_Gaz_place_national.txt'
csv_file = 'Backend/2024_Gaz_place_national_processed.csv'
walk_file = 'Backend/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv'
processed_walk_file = 'Backend/walkability_index_processed.csv'

# convert gazetter file from txt to csv
txt_to_csv(txt_file, 'Backend/2024_Gaz_place_national_processed.csv')

# load city mapping data
df_gaz = pd.read_csv(csv_file, dtype={"GEOID": str, "NAME": str})

# POSSIBLE ISSUES HERE DEBUGGING STILL
def normalize_place_name(name):
    name = name.lower()
    name = re.sub(r'\s+', '', name)
    name = re.sub(r'(city|town|village|CDP|municipality|borough)$', '', name)
    name = re.sub(r'[^/w]', '', name)
    return name

# convert to dictionary
city_lookup = df_gaz.set_index("GEOID")["NAME"].to_dict()

# get city name from constructed 12 digit GEOID
def get_city_name_from_geoid(geoid_12digit):
    # first 5 digits are state and county
    state_county_code = geoid_12digit[:5]

    # first 7 digits are state, county, and place
    place_geoid = geoid_12digit[:7]

    # matching 7 digit GEOID
    city = city_lookup.get(place_geoid, "Unknown City")
    if city != "Unknown City":
        print(f"Found city for 7-digit GEOID: {city}")
        return city
    
    # if no match, try 5 digit GEOID
    city = city_lookup.get(state_county_code, "Unknown City")
    if city != "Unknown City":
        print(f"Found city for 5-digit GEOID: {city}")
    return city

name_to_geoid = {normalize_place_name(v): k for k, v in city_lookup.items()}

# load walkability data
df_walk = pd.read_csv(walk_file)

# generate 12 digit GEOID column
df_walk['GEOID_12digit'] = (
    df_walk['STATEFP'].astype(str).str.zfill(2) +
    df_walk['COUNTYFP'].astype(str).str.zfill(3) +
    df_walk['TRACTCE'].astype(str).str.zfill(6) +
    df_walk['BLKGRPCE'].astype(str).str.zfill(1)
)

def get_walkability_from_place(place):
    place_geoid = name_to_geoid.get(place)
    if not place_geoid:
        print(f"no GEOID found for place name")
        return None
    matching_rows = df_walk[df_walk['GEOID_12digit'].str.startswith(place_geoid)]
    if matching_rows.empty:
        print(f"no walkability data found for: {place}")
        return None
    print(f"found{len(matching_rows)} records for {place}")
    return matching_rows

# CHECKPOINT:
place_search = "bunker hill"
walkability_info = get_walkability_from_place(place_search)
if walkability_info is not None:
    print(walkability_info.head())