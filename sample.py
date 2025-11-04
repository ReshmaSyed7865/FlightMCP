import requests
from mcp.server.fastmcp import FastMCP
from typing import List
import requests
API_URL = "http://localhost:5000/add_flight"  # Replace with your actual endpoint
 # Create MCP server
mcp = FastMCP("FlightManager")
@mcp.tool()
def add_flight_mcp(flight_id: int, flight_name: str, source: str, destination: str, seats: int) -> str:
    """Call API to add a flight to the database."""
    payload = {
        "flight_id": flight_id,
        "flight_name": flight_name,
        "source": source,
        "destination": destination,
        "number_of_seats": seats
    }
 
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return "Flight added successfully."
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"API call failed: {str(e)}"
add_flight_mcp(7,"ABC","CHN","DBI",10)
