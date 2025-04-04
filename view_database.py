import sqlite3

database = "climate_walkability.db"

conn = sqlite3.connect(database)
cursor = conn.cursor()

# View all data
cursor.execute("SELECT * FROM geocoded_addresses")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Delete all data after searching
cursor.execute("DELETE FROM geocoded_addresses")
conn.commit()

conn.close()
print("Database cleared after searching.")

# how to get walkability data from this?