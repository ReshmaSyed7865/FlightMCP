import sqlite3
import random
 
# Connect to SQLite database
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()
 
# Drop existing tables if any
cursor.execute("DROP TABLE IF EXISTS flights")
cursor.execute("DROP TABLE IF EXISTS seats")
 
# Create flights table
cursor.execute('''
    CREATE TABLE flights (
        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_name TEXT,
        source TEXT,
        destination TEXT,
        number_of_seats INTEGER -- this now means available seats only
    )
''')
 
# Create seats table
cursor.execute('''
    CREATE TABLE seats (
        seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id INTEGER,
        seat_number TEXT,
        availability TEXT CHECK(availability IN ('available', 'booked')),
        FOREIGN KEY(flight_id) REFERENCES flights(flight_id)
    )
''')
 
# Sample data
flight_names = ["Indigo", "Air India", "SpiceJet", "GoAir", "Vistara"]
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Hyderabad", "Kolkata"]
 
for name in flight_names:
    src, dest = random.sample(cities, 2)
    total_seats = 10
    available_count = 0
 
    # Insert a placeholder flight record
    cursor.execute('''
        INSERT INTO flights (flight_name, source, destination, number_of_seats)
        VALUES (?, ?, ?, ?)
    ''', (name, src, dest, 0))
    flight_id = cursor.lastrowid
 
    # Insert seat records
    for i in range(1, total_seats + 1):
        seat_num = f"{i:02d}A"
        availability = random.choice(["available", "booked"])
        if availability == "available":
            available_count += 1
        cursor.execute('''
            INSERT INTO seats (flight_id, seat_number, availability)
            VALUES (?, ?, ?)
        ''', (flight_id, seat_num, availability))
 
    # Update the flight with correct available seat count
    cursor.execute('''
        UPDATE flights SET number_of_seats = ? WHERE flight_id = ?
    ''', (available_count, flight_id))
 
conn.commit()
conn.close()
print("Database created with available seat counts.")
 
