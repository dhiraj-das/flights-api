from typing import Union
from fast_flights import FlightData, Passengers, Result, get_flights
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Flight(BaseModel):
    origin: str
    destination: str
    start_date: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/flights/")
async def search_flight():
    result: Result = get_flights(
        flight_data=[
            FlightData(date="2025-03-03", from_airport="GAU", to_airport="DEL")
        ],
        trip="one-way",
        seat="economy",
        passengers=Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0),
        fetch_mode="fallback",
    )
    return result

@app.post("/flight/")
async def create_flight(flight: Flight):
    result: Result = get_flights(
        flight_data=[
            FlightData(date=flight.start_date, from_airport=flight.origin, to_airport=flight.destination)
        ],
        trip="one-way",
        seat="economy",
        passengers=Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0),
        fetch_mode="fallback",
    )

    response = {
        "price_type": result.current_price,
        "flights": result.flights[0:3]
    }

    return response


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}