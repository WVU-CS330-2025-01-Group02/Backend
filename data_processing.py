import requests
import sqlite3
import csv

# census geocoder api batch processing
CENSUS_BATCH_URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
CENSUS_BENCHMARK = "Public_AR_Current"

def create_database(source):
    conn = sqlite3.connect(source)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS geocoded_addresses (
            id INTEGER PRIMARY KEY,
            street TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            latitude REAL,
            longitude REAL
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
    
def parse_batch_response(response_text):
    address_data = []
    reader = csv.reader(response_text.splitlines())

    for row in reader:
        if len(row) >= 7 and "Match" in row[2]:
            try:
                unique_id = row[0]
                street = row[1]
                city = row[1].split(",")[-3].strip()  # Extract city
                state = row[1].split(",")[-2].strip()  # Extract state
                zip_code = row[1].split(",")[-1].strip()  # Extract ZIP
                coordinates = row[5]  # The lat/lon are in this column
                lon, lat = map(float, coordinates.split(","))
                address_data.append((street, city, state, zip_code, lat, lon))
            except ValueError:
                print(f"WARNING: SKIPPING ROW DUE TO INVALID COORDINATES - {row}")

    return address_data

def store_geocoded_data(database, address_data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO geocoded_addresses (street, city, state, zip, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', address_data)
    conn.commit()
    conn.close()

def process_addresses(input_csv, database):
    batch_csv = "batch_addresses.csv"
    create_database(database)
    write_batch_file(input_csv, batch_csv)
    response_text = query_census_batch(batch_csv)
    if response_text:
        address_data = parse_batch_response(response_text)
        store_geocoded_data(database, address_data)
        print("batch geocoding completed and stored successfully")
    else:
        print("no response from census api")

if __name__ == "__main__":
    input_csv = "addresses.csv"
    database = "climate_walkability.db"
    process_addresses(input_csv, database)