import sqlite3
import json
import sys
 
def get_all_flights():
    conn = sqlite3.connect('db/flightss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()
 
    result = [dict(zip(col_names, row)) for row in flights]
    print(json.dumps(result))  # Print to stdout
 
if __name__ == "__main__":
    if sys.argv[1] == 'all_flights':
        get_all_flights()
