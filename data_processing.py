import requests
import sqlite3
import csv
import os

# census geocoder api batch processing
SLD_CSV = "EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv"
CENSUS_BATCH_URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
CENSUS_GEO_URL = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
CENSUS_BENCHMARK = "Public_AR_Current"

def create_database(source):
    conn = sqlite3.connect(source)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS geocoded_addresses')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS geocoded_addresses (
            id INTEGER PRIMARY KEY,
            street TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            latitude REAL,
            longitude REAL,
            block_group_geoid TEXT,
            intersection_density REAL,
            residential_density REAL,
            transit_access REAL
    )
    ''')
    conn.commit()
    conn.close()

def write_batch_file(input_csv, batch_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, open(batch_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        next(reader)
        for i, row in enumerate(reader):
            unique_id, street, city, state, zip_code = row
            writer.writerow([i, street, city, state, zip_code])

def query_census_batch(batch_csv):
    with open(batch_csv, 'rb') as batch_file:
        file = {'addressFile': batch_file}
        params = {'benchmark': CENSUS_BENCHMARK}
        response = requests.post(CENSUS_BATCH_URL, files={'addressFile': batch_file}, params=params)

    if response.status_code == 200:
        print(response.text)
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None
    
def get_block_group_geoid(lat, lon):
    params = {
        "x": lon,
        "y": lat,
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "format": "json"
    }
    response = requests.get(CENSUS_GEO_URL, params=params)
    print(f"API response for {lat}, {lon}: {response.json()}")
    try:
        data = response.json()
        full_geoid = data["result"]["geographies"]["Census Blocks"][0]["GEOID"]
        return full_geoid[:12]
    except (KeyError, IndexError):
        print(f"Failed to get GEOID for {lat}, {lon}")
        return None

def load_sld(filepath):
    sld_data = {}
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            geoid = row["BLKGRPCE"]
            sld_data[geoid] = row
    return sld_data

def parse_batch_response(response_text, sld_data):
    address_data = []
    reader = csv.reader(response_text.splitlines())
    for row in reader:
        if len(row) >= 7 and "Match" in row[2]:
            try:
                street = row[1]
                city = row[1].split(",")[-3].strip()
                state = row[1].split(",")[-2].strip()
                zip_code = row[1].split(",")[-1].strip()
                lon, lat = map(float, row[5].split(","))
                block_group = get_block_group_geoid(lat, lon)
                sld_row = sld_data.get(block_group, {})
                int_density = float(sld_row.get("D3b", -1))
                res_density = float(sld_row.get("D2a_EPHHM", -1))
                transit = float(sld_row.get("D5ar", -1))
                address_data.append((street, city, state, zip_code, lat, lon, block_group, int_density, res_density, transit))
            except ValueError:
                print(f"WARNING: Skipping row with invalid coordinates - {row}")
    return address_data

def store_geocoded_data(database, address_data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO geocoded_addresses 
        (street, city, state, zip, latitude, longitude, block_group_geoid, intersection_density, residential_density, transit_access)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', address_data)
    conn.commit()
    conn.close()

def process_addresses(input_csv, database):
    batch_csv = "batch_addresses.csv"
    create_database(database)
    write_batch_file(input_csv, batch_csv)
    response_text = query_census_batch(batch_csv)
    if response_text:
        sld_data = load_sld(SLD_CSV)
        address_data = parse_batch_response(response_text, sld_data)
        store_geocoded_data(database, address_data)
        print("walkability data stored successfully")
    else:
        print("no response from census api")

if __name__ == "__main__":
    input_csv = "addresses.csv"
    database = "climate_walkability.db"
    process_addresses(input_csv, database)