DROP TABLE IF EXISTS geocoded_addresses;

CREATE TABLE geocoded_addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    streeet TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);