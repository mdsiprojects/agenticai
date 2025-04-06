from pydantic import BaseModel, Field
from agents import function_tool
import requests

import random

from dotenv import load_dotenv
from agents import (

    Agent,
    Runner,
    RunConfig,
    trace,
    ModelSettings,
    handoff
)
load_dotenv()


from helpers.trace_util import get_trace_url

from helpers.model_client import (
    get_openai_client,
    get_github_model_provider
)



@function_tool
def get_wttn_function(city: str) -> str:
    """Get the weather for a given city"""
    print(f"[debug] get_wttn called with city: {city}")
    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}")
    return response.text


class WttnReport(BaseModel):
    city: str = Field(..., description="The name of the city")
    temperature: str = Field(..., description="The temperature in the city")
    feels_like: str = Field(..., description="The feels like temperature in the city")
    conditions: str = Field(..., description="The weather conditions in the city")
    wind_speed: str = Field(..., description="The wind speed in the city")
    wind_direction: str = Field(..., description="The wind direction in the city")
    precepitation: str = Field(..., description="The precepitation in the city")
    humidity: str = Field(..., description="The humidity in the city")
    location_logLat: str = Field(..., description="The latitude of the city")
    location_logLong: str = Field(..., description="The longitude of the city")


class WttnPeriodReport(BaseModel):
    weekday: str = Field(..., description="The name of the week day")
    periodofday: str = Field(..., description="The period of the day for example Morning, Noon, Evening and Night")
    periodforecast: WttnReport = Field(..., description="The weather report for the period of the day")


class WttnFullReport(BaseModel):
    weather_now: WttnReport = Field(..., description="The current weather report")
    weather_forecast_day1: list[WttnPeriodReport] = Field(..., description="The weather forecast for the first day in the report")
    weather_forecast_day2: list[WttnPeriodReport] = Field(..., description="The weather forecast for the second day in the report")
    weather_forecast_day3: list[WttnPeriodReport] = Field(..., description="The weather forecast for the third day in the repor")
    weather_wttn_raw_response: str = Field(..., description="The raw response from the wttr.in API")



def sample_wttn_response():
    return """
[debug-server] get_current_weather(London)
Weather report: London

     \  /       Partly cloudy
   _ /"".-.     +7(4) °C
     \_(   ).   ↙ 18 km/h
     /(___(__)  10 km
                0.0 mm
                                                       ┌─────────────┐
┌──────────────────────────────┬───────────────────────┤  Sat 05 Apr ├───────────────────────┬──────────────────────────────┐
│            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │     \   /     Clear          │
│      .-.      +12(10) °C     │      .-.      17 °C          │      .-.      +12(10) °C     │      .-.      +8(5) °C       │
│   ― (   ) ―   ↙ 18-21 km/h   │   ― (   ) ―   ↙ 20-23 km/h   │   ― (   ) ―   ↙ 18-24 km/h   │   ― (   ) ―   ↙ 17-24 km/h   │
│      `-’      10 km          │      `-’      10 km          │      `-’      10 km          │      `-’      10 km          │
│     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                                       ┌─────────────┐
┌──────────────────────────────┬───────────────────────┤  Sun 06 Apr ├───────────────────────┬──────────────────────────────┐
│            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │     \   /     Clear          │
│      .-.      +11(8) °C      │      .-.      +13(11) °C     │      .-.      +10(8) °C      │      .-.      +7(5) °C       │
│   ― (   ) ―   ↙ 21-24 km/h   │   ― (   ) ―   ← 22-25 km/h   │   ― (   ) ―   ↙ 17-21 km/h   │   ― (   ) ―   ↙ 13-20 km/h   │
│      `-’      10 km          │      `-’      10 km          │      `-’      10 km          │      `-’      10 km          │
│     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                                       ┌─────────────┐
┌──────────────────────────────┬───────────────────────┤  Mon 07 Apr ├───────────────────────┬──────────────────────────────┐
│            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │     \   /     Clear          │
│      .-.      +10(9) °C      │      .-.      +14(12) °C     │      .-.      +11(10) °C     │      .-.      +8(7) °C       │
│   ― (   ) ―   ← 10-12 km/h   │   ― (   ) ―   ← 14-16 km/h   │   ― (   ) ―   ← 11-15 km/h   │   ― (   ) ―   ← 8-12 km/h    │
│      `-’      10 km          │      `-’      10 km          │      `-’      10 km          │      `-’      10 km          │
│     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
Location: London, Greater London, England, UK [51.5073219,-0.1276474]

Follow @igor_chubin for wttr.in updates

"""


def get_attn_report_output() -> str:
    return """
        in this report for example you can see that the weather in London now is:
        Partly cloudy, with a temperature of +7(4) °C and wind speed of 18 km/h.
        The report also provides the weather forecast for the next 3 days:
        - Saturday 05 Apr:
            - Morning: Sunny, with a temperature of +12(10) °C and wind speed of 18-21 km/h south west
            - Noon: Sunny, with a temperature of 17 °C and wind speed of 20-23 km/h south west
            - Evening: Sunny, with a temperature of +12(10) °C and wind speed of 18-24 km/h south west
            - Night: Clear, with a temperature of +8(5) °C and wind speed of 17-24 km/h south west
        also from the report you can see that on Monday 07 Apr the weather is:
            - Morning: Sunny, with a temperature of +10(9) °C and wind speed of 10-12 km/h westerly
            - Noon: Sunny, with a temperature of +14(12) °C and wind speed of 14-16 km/h westerly
            - Evening: Sunny, with a temperature of +11(10) °C and wind speed of 11-15 km/h westerly
            - Night: Clear, with a temperature of +8(7) °C and wind speed of 8-12 km/h westerly

        precepitation is 0.0 mm and humidity is 0 percent  at all times

        London is located at latitude 51.5073219 and longitude -0.1276474


"""



def get_attn_agent(agent_name="weather_and_location_agent") -> Agent:
    """
    Get the agent for the given agent name.
    """
    # Create the agent with the specified tools and model settings

    summariser_agent = Agent(
        name="whether_report_summariser_agent",
        model="o3-mini",
        tools=[],
        model_settings=ModelSettings(**{"max_tokens": 16000}),
        output_type=str,
        instructions=f"""
        you can read a detailed structured weather report, and then write a weather report summary for the user.
        the summary can be ready by a human and should be easy to understand.
        the report should include information about the weather conditions now,
        summary of changes in the weather over the next three days,
        with special attention to any extreme changes during the day or over the next few days
        """,
        handoff_description = "You are writing a weather report summary for the user from structured and detailed weather report data",

        )


    weather_data_collector = Agent(
        name="weather_data_collector",
        tools=[get_wttn_function],
        handoffs=[],
        model_settings=ModelSettings(**{"max_tokens": 16000}),
        output_type=WttnFullReport,
        instructions=f"""
        You are a weather and location agent. You can answer questions about the weather and locations.
        You can also provide a weather report for a given city.
        You can also provide a weather forecast for the next 3 days for a given city.
        You can also provide the latitude and longitude of a given location.

        you can read a raw weather report like this one and understand it:
        {sample_wttn_response()}

        and understand that following details from this input:
        {get_attn_report_output()}

        you will make a all to the wttn API to get the weather report for a given city.

        and you will return a structured weather report and raw response from the API

        """
    )


    weather_agent = Agent(
        name="weather_agent",
        tools=[weather_data_collector.as_tool(
            tool_name = "weather_data_collector",
            tool_description = "you collect data about weather from different data sources for a given city or location"
        )],
        handoffs=[summariser_agent],
        model_settings=ModelSettings(**{"max_tokens": 16000}),
        output_type=str,
        instructions=f"""
        You are a weather and location agent.
        You can answer questions about the weather and locations.
        You orchestrate the process of data collection and writing the weather report summary.
        write your report in Mardown format.
        Your report should be detailed and comprehensive
        """,
        tool_use_behavior="run_llm_again"
    )

    return weather_agent

