DROP TABLE IF EXISTS geocoded_addresses;

CREATE TABLE geocoded_addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
    block_group_geoid TEXT,
    intersection_density REAL
    residential_density REAL,
    transit_access REAL
);