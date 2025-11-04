from flask import Flask, request, jsonify
import sqlite3
 
app = Flask(__name__)
 
def db_connection():
    conn = sqlite3.connect("flights.db")
    conn.row_factory = sqlite3.Row
    return conn
 
# Add flight
@app.route('/')
def hello():
    return "Hi"
@app.route('/add_flight', methods=['POST'])
def add_flight():
    data = request.get_json()
    flight_number = data['flight_number']
    origin = data['origin']
    destination = data['destination']
    seat = data.get('seat', 'available')
 
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flights (flight_number, origin, destination, seat) VALUES (?, ?, ?, ?)",
                   (flight_number, origin, destination, seat))
    conn.commit()
    conn.close()
 
    # return jsonify({"message": "Flight added successfully"}), 201
    return "flight added"
 
# Get flight info
@app.route('/flights', methods=['GET'])
def get_flights():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    rows = cursor.fetchall()
    conn.close()
 
    flights = [dict(row) for row in rows]
    return jsonify(flights), 200
 
# Select seat
@app.route('/select_seat', methods=['GET','POST'])
def select_seat():
    data = request.get_json()
    flight_id = data['id']
    conn = db_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT seat FROM flights WHERE id = ?", (flight_id,))
    row = cursor.fetchone()
    
    if row and row['seat'] == 'available':
        cursor.execute("UPDATE flights SET seat = 'booked' WHERE id = ?", (flight_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Seat booked successfully"}), 200
    else:
        conn.close()
        return jsonify({"message": "Seat already booked or flight not found"}), 404
 
if __name__ == '__main__':
 app.run(debug=True)
