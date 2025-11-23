"""Weather MCP client wrapper for fetching historical weather data.

This handles connection to Weather MCP server for historical weather lookups.
Used in Room 1 (first date weather) and Room 2 (accident night weather).
"""

import logging
import os
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


async def connect_to_weather_mcp():
    """Connect to Weather MCP server (if enabled).

    Returns:
        Weather MCP client or MockWeatherMCPClient if disabled
    """
    # Check if Weather MCP is enabled
    enable_weather = os.getenv("ENABLE_WEATHER_MCP", "false").lower() == "true"

    if not enable_weather:
        logger.info("[WEATHER_MCP] Using mock weather data (ENABLE_WEATHER_MCP=false)")
        return MockWeatherMCPClient()

    try:
        # TODO: Implement actual Weather MCP connection
        # For now, return mock client
        logger.warning("[WEATHER_MCP] Weather MCP server connection not yet implemented")
        logger.info("[WEATHER_MCP] Using mock data. To enable: Install Weather MCP server")
        return MockWeatherMCPClient()

    except Exception as e:
        logger.error(f"[WEATHER_MCP] Failed to connect to Weather MCP server: {e}")
        return MockWeatherMCPClient()


class MockWeatherMCPClient:
    """Mock Weather MCP client with realistic historical weather data.

    Provides simulated weather data for demo/testing without actual Weather MCP server.
    """

    def __init__(self):
        # Pre-configured weather data for common demo scenarios
        self.weather_database = {
            # First date (October 2023) - Rainy day
            "2023-10-15_seattle": {
                "date": "2023-10-15",
                "location": "Seattle, WA",
                "condition": "Light rain",
                "temperature": 52,
                "humidity": 78,
                "cloud_cover": "Overcast",
                "precipitation": 0.2,
                "wind_speed": 8
            },
            # Accident night (March 2024) - Heavy rain
            "2024-03-03_seattle": {
                "date": "2024-03-03",
                "time": "23:47",
                "location": "Seattle, WA",
                "condition": "Heavy rain",
                "temperature": 45,
                "humidity": 92,
                "cloud_cover": "Overcast",
                "precipitation": 0.8,
                "wind_speed": 15,
                "wind_gusts": 25,
                "visibility": 500,  # feet
                "road_conditions": "Wet, hydroplaning risk HIGH"
            }
        }

    async def call_tool(self, tool_name: str, arguments: dict) -> Dict[str, Any]:
        """Mock tool calling for weather data.

        Args:
            tool_name: Name of the tool (e.g., "get_historical_weather")
            arguments: Tool arguments (date, location, time)

        Returns:
            Weather data dictionary
        """
        if tool_name == "get_historical_weather":
            date = arguments.get("date")
            location = arguments.get("location", "Seattle, WA")
            time = arguments.get("time")

            # Normalize location
            location_key = location.lower().replace(" ", "").replace(",", "_")
            if "seattle" in location_key:
                location_key = "seattle"

            # Create lookup key
            lookup_key = f"{date}_{location_key}"

            if lookup_key in self.weather_database:
                logger.info(f"[WEATHER_MCP] Retrieved weather for {date} in {location}")
                return self.weather_database[lookup_key]
            else:
                # Generate reasonable default weather
                logger.warning(f"[WEATHER_MCP] No data for {lookup_key}, generating default")
                return self._generate_default_weather(date, location, time)

        else:
            logger.warning(f"[MOCK_WEATHER_MCP] Unknown tool: {tool_name}")
            return {}

    def _generate_default_weather(self, date: str, location: str, time: Optional[str] = None) -> Dict[str, Any]:
        """Generate reasonable default weather data.

        Args:
            date: Date string (YYYY-MM-DD)
            location: Location string
            time: Optional time string (HH:MM)

        Returns:
            Weather data dictionary
        """
        # Parse month for seasonal variation
        try:
            month = int(date.split("-")[1])
        except:
            month = 6

        # Seasonal conditions
        if month in [12, 1, 2]:  # Winter
            condition = "Cloudy"
            temp = 40
        elif month in [3, 4, 5]:  # Spring
            condition = "Light rain"
            temp = 55
        elif month in [6, 7, 8]:  # Summer
            condition = "Partly cloudy"
            temp = 72
        else:  # Fall
            condition = "Overcast"
            temp = 58

        weather_data = {
            "date": date,
            "location": location,
            "condition": condition,
            "temperature": temp,
            "humidity": 65,
            "cloud_cover": "Overcast",
        }

        if time:
            weather_data["time"] = time

        return weather_data

    async def get_historical_weather(self, date: str, location: str = "Seattle, WA", time: Optional[str] = None) -> Dict[str, Any]:
        """Convenience method for getting historical weather.

        Args:
            date: Date string (YYYY-MM-DD)
            location: Location string (default: Seattle, WA)
            time: Optional time string (HH:MM)

        Returns:
            Weather data dictionary
        """
        arguments = {"date": date, "location": location}
        if time:
            arguments["time"] = time

        return await self.call_tool("get_historical_weather", arguments)
