from pydantic import BaseModel, Field
from agents import function_tool

import random


class Weather(BaseModel):
    city: str
    temperature: str
    conditions: str


class CurrentTime(BaseModel):
    location: str = Field(..., description="The name of the location")
    current_time: str = Field(..., description="The time in location")


@function_tool
def get_weather(city: str) -> Weather:
    print(f"[debug] getting weather for {city}")
    temperature = f"{random.randint(-10, 50)}C"
    conditions = random.choice(["Sunny", "Windy", "Rainy", "Cloudy"])
    return Weather(city=city, temperature=temperature, conditions=conditions)


@function_tool
def get_current_time(location) -> CurrentTime:
    from datetime import datetime
    """Get the current time for a given location"""
    print(f"[debug] get_current_time called with location: {location}")
    location_lower = location.lower()

    current_time = datetime.now().strftime("%I:%M %p")
    return CurrentTime(
        location=location_lower,
        current_time=current_time,
    )
