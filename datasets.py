# import statements
import pandas as pd
import requests
import time
import re
import fiona
import geopandas as gpd

# DEBUGGING
print("fiona version", fiona.__version__)
print("geopandas version:", gpd.__version__)

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
shapefile_WV = 'Backend/tl_2024_54_place/tl_2024_54_place.shp'

# THIS LINE IS NOT WORKING
gdf_places_WV = gpd.read_file(shapefile_WV)

# DEBUGGING
print(gdf_places_WV.head())

# GEOIDS ARE NOT MATCHING BETWEEN GAZETTER AND WALKABILITY FILES
# TRYING TO USE TIGER FILES

# convert gazetter file from txt to csv
txt_to_csv(txt_file, 'Backend/2024_Gaz_place_national_processed.csv')

# load city mapping data
df_gaz = pd.read_csv(csv_file, dtype={"GEOID": str, "NAME": str})

# convert to dictionary
city_lookup = df_gaz.set_index("GEOID")["NAME"].to_dict()

# for not exact inputs
def fuzzy_place_lookup(place):
    for name in name_to_geoid:
        if place.lower() in name.lower():
            print(f"Matched input '{place}' to gazetteer name '{name}'")
            return name_to_geoid[name]
    print(f"No match found for '{place}'")
    return None

# get city name from constructed 12 digit GEOID
def get_city_name_from_geoid(geoid_12digit):
    for digits in [7, 5]:
        prefix = geoid_12digit[:digits]
        city = city_lookup.get(prefix)
        if city:
            print(f"Found city for {digits}-digit GEOID prefix: {city}")
            return city
    return "Unknown City"

name_to_geoid = {v: k for k, v in city_lookup.items()}

# load walkability data
df_walk = pd.read_csv(walk_file)

# generate 12 digit GEOID column
df_walk['GEOID_12digit'] = (
    df_walk['STATEFP'].astype(str).str.zfill(2) +
    df_walk['COUNTYFP'].astype(str).str.zfill(3) +
    df_walk['TRACTCE'].astype(str).str.zfill(6) +
    df_walk['BLKGRPCE'].astype(str).str.zfill(1)
)

# Add GEOID prefix to EPA data
df_walk['GEOID_prefix5'] = df_walk['GEOID_12digit'].str[:5]
df_walk['GEOID_prefix7'] = df_walk['GEOID_12digit'].str[:7]

# And try matching with place GEOIDs
df_gaz['GEOID_prefix5'] = df_gaz['GEOID'].str[:5]
df_gaz['GEOID_prefix7'] = df_gaz['GEOID'].str[:7]

# get walkability from place
def get_walkability_from_place(place):
    place_geoid = fuzzy_place_lookup(place)
    if not place_geoid:
        print(f"No GEOID found for place name '{place}'")
        return None

    # Try 7-digit prefix match (state+county+place)
    matched_rows_7 = df_walk[df_walk['GEOID_prefix7'] == place_geoid[:7]]
    if not matched_rows_7.empty:
        print(f"Found {len(matched_rows_7)} records for {place} using 7-digit prefix")
        return matched_rows_7

    # Try 5-digit prefix match (state+county)
    matched_rows_5 = df_walk[df_walk['GEOID_prefix5'] == place_geoid[:5]]
    if not matched_rows_5.empty:
        print(f"Found {len(matched_rows_5)} records for {place} using 5-digit prefix")
        return matched_rows_5

    print(f"No walkability data found for: {place}")
    return None