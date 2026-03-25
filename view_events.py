import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

print("\n=== All Stored Events ===")
cursor.execute("SELECT * FROM events ORDER BY date")
rows = cursor.fetchall()

if not rows:
    print("No events stored yet.")
else:
    for row in rows:
        band, city, date = row
        print(f"Band: {band} | City: {city} | Date: {date}")

print(f"\nTotal events stored: {len(rows)}")
connection.close()