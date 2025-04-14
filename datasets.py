# import statements
import pandas as pd
import requests
import time
import re

# TO DO!
# DOWNLOAD BLOCK GROUP SHAPEFILES FROM CENSUS
# INSTALL GEOPANDAS AND SHAPELY
# CALCULATE CENTROIDS FROM SHAPEFILE
# MERGE WALKABILITY AND CENTROIDS
# UPDATE GET WALKABILITY FROM PLACE TO RELY ON COORDINATES
# FIND NEAREST NEIGHBOR IN DATASET

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

# load walkability data
df_walk = pd.read_csv(walk_file)

# convert to dictionary
city_lookup = df_gaz.set_index("GEOID")["NAME"].to_dict()
name_to_geoid = {v: k for k, v in city_lookup.items()}

# for not exact inputs
def fuzzy_place_lookup(place):
    for name in name_to_geoid:
        if place.lower() in name.lower():
            print(f"\nMatched input '{place}' to gazetteer name '{name}'\n"
                 "=======================================================================" \
                )
            geoid = str(name_to_geoid[name].zfill(7))
            return geoid
    print(f"No match found for '{place}'")
    return None

# generate 12 digit GEOID column
df_walk['GEOID_12digit'] = (
    df_walk['STATEFP'].astype(str).str.zfill(2) +
    df_walk['COUNTYFP'].astype(str).str.zfill(3) +
    df_walk['TRACTCE'].astype(str).str.zfill(6) +
    df_walk['BLKGRPCE'].astype(str).str.zfill(1)
)

# get walkability from place
def get_walkability_from_place(place):
    place_geoid = fuzzy_place_lookup(place)
    if not place_geoid:
        print(f"No GEOID found for place name '{place}'")
        return None
    
    # does not work, walkability data and gazetter files use different types of geoids
    matching_rows = df_walk[df_walk['GEOID_12digit'].str[2:7] == place_geoid]
    if not matching_rows.empty:
        print(f"\nFound {len(matching_rows)} matching block groups for GEOID {place_geoid} in {place}\n")
        # add return statement to fetch walkability data
    else:
        print(f"No walkability data found for: {place}")
        return None

# DEBUGGING
print(get_walkability_from_place("los angeles"))
print(get_walkability_from_place("Morgantown"))
print(get_walkability_from_place("MARIETTA"))
print(get_walkability_from_place("not a real town"))

print(fuzzy_place_lookup("los angeles"))
print(fuzzy_place_lookup("Morgantown"))
print(fuzzy_place_lookup("MARIETTA"))