from mcp.server.fastmcp import FastMCP
from typing import List
import requests
 # Create MCP server
mcp = FastMCP("FlightManager")

@mcp.tool()
def add_flight(flight_id: int, flight_name: str, source: str, destination: str, seats: int) -> str:
    """Call API to add a flight to the database."""
    payload = {
        "flight_id": flight_id,
        "flight_name": flight_name,
        "source": source,
        "destination": destination,
        "number_of_seats": seats
    }
    API_URL="http://127.0.0.1:5000/add_flight"
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return "Flight added successfully."
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"API call failed: {str(e)}"
@mcp.tool()
def flight_list():
    res=requests.get("http://127.0.0.1:5000/get_flight")
    output=res.json()
    print(output)
    return output

@mcp.tool()
def flight_available():
    res=requests.get("http://127.0.0.1:5000/flights/check_flight_availability")
    output=res.json()
    print(output)
    return output
@mcp.tool()
def seat_available():
    res=requests.get("http://127.0.0.1:5000/flights/check_seat_availability")
    output=res.json()
    print(output)
    return output
    
@mcp.tool()
def flight_booking(flight_id:int,seat_id:str)->str:
    """Call API to add a flight to the database."""
    payload = {
        "flight_id": flight_id,
        "seat_number":seat_id
    }
    API_URL="http://127.0.0.1:5000/select_seat"
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return "Seat booked successfully."
        elif response.status_code==404:
           return "Seat already booked(unavailable)"
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"API call failed: {str(e)}"
   



# # Resource: Greeting
# @mcp.tool()
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}! How can I assist you with leave management today?"

if __name__ == "__main__":
    mcp.run()
