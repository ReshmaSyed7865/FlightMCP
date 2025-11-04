from flask import Flask, request, jsonify
import sqlite3
 
app = Flask(__name__)
DB_NAME = 'flights.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def hello():
    return "Hi"
# 1. Add Flight (POST)
@app.route('/add_flight', methods=['POST'])
def add_flight():
    data = request.get_json()
    print(data)
    flight_name = data['flight_name']
    source = data['source']
    destination = data['destination']
    total_seats = data.get('total_seats', 10)
 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flights (flight_name, source, destination, number_of_seats) VALUES (?, ?, ?, ?)",
                   (flight_name, source, destination, total_seats))
    flight_id = cursor.lastrowid
 
    for i in range(1, total_seats + 1):
        seat_num = f"{i:02d}A"
        cursor.execute("INSERT INTO seats (flight_id, seat_number, availability) VALUES (?, ?, ?)",
                       (flight_id, seat_num, 'available'))
 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Flight added successfully', 'flight_id': flight_id})
 
# 2. Get Flight Info (GET)
@app.route('/get_flight', methods=['GET'])
def get_flight():
    flight_id = request.args.get('flight_id')
    conn = get_db_connection()
    cursor = conn.cursor()
 
    if flight_id:
        cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
    else:
        cursor.execute("SELECT * FROM flights")
        
    flights = cursor.fetchall()
    result = [dict(row) for row in flights]
    conn.close()
    return jsonify(result)
 
# 3. Select Seat (POST)
@app.route('/select_seat', methods=['POST'])
def select_seat():
    data = request.get_json()
    flight_id = data['flight_id']
    seat_number = data['seat_number']
 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT availability FROM seats WHERE flight_id = ? AND seat_number = ?",
                   (flight_id, seat_number))
    row = cursor.fetchone()
 
    if not row:
        conn.close()
        return jsonify({'error': 'Seat not found'}), 404
 
    if row['availability'] == 'booked':
        conn.close()
        return jsonify({'error': 'Seat already booked'}), 400
 
    # Update seat to booked
    cursor.execute("UPDATE seats SET availability = 'booked' WHERE flight_id = ? AND seat_number = ?",
                   (flight_id, seat_number))
 
    # Update flight available seat count
    cursor.execute("UPDATE flights SET number_of_seats = number_of_seats - 1 WHERE flight_id = ?",
                   (flight_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Seat {seat_number} booked successfully'})
 
# 4. Check Availability (GET)
@app.route('/check_flight_availability', methods=['GET'])
def check_flight_availability():
    flight_id = request.args.get('flight_id')
    conn = get_db_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT number_of_seats FROM flights WHERE flight_id = ?", (flight_id,))
    row = cursor.fetchone()
    conn.close()
 
    if not row:
        return jsonify({'error': 'Flight not found'}), 404
 
    return jsonify({'flight_id': flight_id, 'available_seats': row['number_of_seats']})
@app.route('/check_seat_availability', methods=['GET'])
def check_seat_availability():
    flight_id = request.args.get('flight_id')
    seat_id=request.args.get('seat_id')
    conn = get_db_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT availability FROM seats WHERE flight_id = ? AND seat_id= ?", (flight_id,seat_id))
    row = cursor.fetchone()
    conn.close()
 
    if not row:
        return jsonify({'error': 'Flight noe founf'}), 404
 
    return jsonify({'flight_id': flight_id,'seat_id':seat_id, 'availability':row['availability']})
 
# Run the Flask app
if __name__ == '__main__':
  app.run(debug=True)
