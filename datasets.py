# import statements
import pandas as pd
import requests
import time

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
txt_file = '2024_Gaz_place_national.txt'
csv_file = '2024_Gaz_place_national_processed.csv'
walk_file = 'walkability_index.csv'
processed_walk_file = 'walkability_index_processed.csv'

# convert gazetter file from txt to csv
txt_to_csv(txt_file, csv_file)

# load city mapping data
df_gaz = pd.read_csv(csv_file, dtype={"GEOID": str, "NAME": str})

# convert to dictionary
city_lookup = df_gaz.set_index("GEOID")["NAME"].to_dict()

# CHECKPOINT: console should display sample of city look ups as
# "Sample of city_lookup: {'100100': 'Abanda CDP', '100124': 'Abbeville city', '100460': 'Adamsville city', '100484': 'Addison town', '100676': 'Akron town'}"
print("Sample of city_lookup:", {k: city_lookup[k] for k in list(city_lookup)[:5]})

# get city name from constructed 12 digit GEOID
def get_city_name_from_geoid(geoid_12digit):
    # first 5 digits are state and county
    state_county_code = geoid_12digit[:5]

    # first 7 digits are state, county, and place
    place_geoid = geoid_12digit[:7]

    # CHECKPOINT: console should display GEOIDs and all information should match
    print(f"Checking GEOID: {geoid_12digit}")
    print(f"Checking for 7-digit match: {place_geoid}")
    print(f"Checking for 5-digit match: {state_county_code}")

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

# load walkability data
df_walk = pd.read_csv(walk_file)

# generate 12 digit GEOID column
df_walk['GEOID_12digit'] = (
    df_walk['STATEFP'].astype(str).str.zfill(2) +
    df_walk['COUNTYFP'].astype(str).str.zfill(3) +
    df_walk['TRACTCE'].astype(str).str.zfill(6) +
    df_walk['BLKGRPCE'].astype(str).str.zfill(1)
)

# CHECKPOINT check head of GEOID12_digit column as
# "First few GEOID_12digit values from walkability data:
# 0    481130078254
# 1    481130078252
# 2    481130078253
# 3    481130078241
# 4    481130078242"
print("First few GEOID_12digit values from walkability data:")
print(df_walk['GEOID_12digit'].head())

# CHECKPOINT test get_city_name_from_geoid as
# Test for GEOID 481130078254:
# Checking GEOID: 481130078254
# Checking for 7-digit match: 4811300
# Checking for 5-digit match: 48113
# Found city for 7-digit GEOID: Bunker Hill Village city
# City for GEOID 481130078254: Bunker Hill Village city
test_geoid = df_walk['GEOID_12digit'].iloc[0]
print(f"Test for GEOID {test_geoid}:")
city = get_city_name_from_geoid(test_geoid)
print(f"City for GEOID {test_geoid}: {city}")

# save new walkability dataset
df_walk.to_csv(processed_walk_file, index=False)
print("Processed walkability data saved.")