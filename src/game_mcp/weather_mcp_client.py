"""Weather MCP client wrapper for fetching historical weather data.

This handles connection to Weather MCP server for historical weather lookups.
Used in Room 1 (first date weather) and Room 2 (accident night weather).

HYBRID MODE:
- If OPENWEATHER_API_KEY is set: Uses real OpenWeather API (authentic MCP)
- Otherwise: Uses mock data (demo/testing mode)
"""

import logging
import os
import aiohttp
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


async def connect_to_weather_mcp():
    """Connect to Weather MCP server (if enabled).

    Returns:
        Weather MCP client (Real API or Mock based on configuration)
    """
    # Check if OpenWeather API key is available
    openweather_key = os.getenv("OPENWEATHER_API_KEY")

    if openweather_key:
        logger.info("[WEATHER_MCP] Using REAL OpenWeather API for historical data")
        return RealWeatherMCPClient(api_key=openweather_key)
    else:
        logger.info("[WEATHER_MCP] Using mock weather data (set OPENWEATHER_API_KEY for real data)")
        return MockWeatherMCPClient()


class RealWeatherMCPClient:
    """Real Weather MCP client using OpenWeather API.

    Uses OpenWeather's free tier API for historical weather data.
    Free tier allows: 1000 calls/day, 60 calls/minute.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        # Note: OpenWeather free tier doesn't have true historical data
        # We use current weather API + mock fallback for past dates
        logger.info("[WEATHER_MCP] Initialized Real Weather API client")

    async def call_tool(self, tool_name: str, arguments: dict) -> Dict[str, Any]:
        """Tool calling interface for weather data.

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

            return await self.get_historical_weather(date, location, time)
        else:
            logger.warning(f"[REAL_WEATHER_MCP] Unknown tool: {tool_name}")
            return {}

    async def get_historical_weather(self, date: str, location: str = "Seattle, WA", time: Optional[str] = None) -> Dict[str, Any]:
        """Get historical weather data.

        Args:
            date: Date string (YYYY-MM-DD)
            location: Location string (default: Seattle, WA)
            time: Optional time string (HH:MM)

        Returns:
            Weather data dictionary
        """
        # Parse location to get city name
        city = location.split(',')[0].strip()

        try:
            # NOTE: OpenWeather free tier doesn't support historical data
            # For demo purposes, we check if date is recent (within 5 days)
            # Otherwise fall back to mock data for puzzle dates

            date_obj = datetime.fromisoformat(date)
            days_ago = (datetime.now() - date_obj).days

            if days_ago > 5:
                # Historical date - use mock data for puzzle answers
                logger.info(f"[WEATHER_MCP] Historical date {date} - using curated data")
                return await self._get_curated_historical_data(date, location, time)
            else:
                # Recent date - fetch from API
                logger.info(f"[WEATHER_MCP] Recent date {date} - fetching from OpenWeather API")
                return await self._fetch_from_api(city, location)

        except Exception as e:
            logger.error(f"[WEATHER_MCP] Error fetching weather: {e}")
            return await self._get_curated_historical_data(date, location, time)

    async def _fetch_from_api(self, city: str, full_location: str) -> Dict[str, Any]:
        """Fetch current/recent weather from OpenWeather API.

        Args:
            city: City name
            full_location: Full location string

        Returns:
            Weather data dictionary
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"  # Fahrenheit
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Map OpenWeather condition codes to readable conditions
                        weather_main = data["weather"][0]["main"]
                        weather_desc = data["weather"][0]["description"]

                        condition_map = {
                            "Rain": "Light rain" if "light" in weather_desc else "Heavy rain",
                            "Drizzle": "Light rain",
                            "Clear": "Clear",
                            "Clouds": "Overcast" if data["clouds"]["all"] > 70 else "Partly cloudy",
                            "Snow": "Snow",
                            "Thunderstorm": "Thunderstorm"
                        }

                        condition = condition_map.get(weather_main, weather_desc.capitalize())

                        logger.info(f"[WEATHER_MCP] Successfully fetched real data for {city}")

                        return {
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "location": full_location,
                            "condition": condition,
                            "temperature": int(data["main"]["temp"]),
                            "humidity": data["main"]["humidity"],
                            "cloud_cover": f"{data['clouds']['all']}%",
                            "wind_speed": int(data["wind"]["speed"])
                        }
                    else:
                        logger.error(f"[WEATHER_MCP] API error: {response.status}")
                        raise Exception(f"API returned {response.status}")

        except Exception as e:
            logger.error(f"[WEATHER_MCP] Failed to fetch from API: {e}")
            raise

    async def _get_curated_historical_data(self, date: str, location: str, time: Optional[str] = None) -> Dict[str, Any]:
        """Get curated historical data for puzzle dates.

        For dates critical to the game narrative, return accurate historical data.

        Args:
            date: Date string
            location: Location string
            time: Optional time string

        Returns:
            Weather data dictionary
        """
        # Critical game dates with accurate historical weather
        curated_database = {
            "2023-10-15_seattle": {
                "date": "2023-10-15",
                "location": "Seattle, WA",
                "condition": "Light rain",  # PUZZLE ANSWER
                "temperature": 52,
                "humidity": 78,
                "cloud_cover": "Overcast",
                "precipitation": 0.2,
                "wind_speed": 8
            },
            "2024-03-03_seattle": {
                "date": "2024-03-03",
                "time": "23:47",
                "location": "Seattle, WA",
                "condition": "Heavy rain",  # Room 3 answer
                "temperature": 45,
                "humidity": 92,
                "cloud_cover": "Overcast",
                "precipitation": 0.8,
                "wind_speed": 15,
                "wind_gusts": 25,
                "visibility": 500,
                "road_conditions": "Wet, hydroplaning risk HIGH"
            }
        }

        # Create lookup key
        city = location.split(',')[0].strip().lower()
        lookup_key = f"{date}_{city}"

        if lookup_key in curated_database:
            logger.info(f"[WEATHER_MCP] Retrieved curated historical data for {date}")
            data = curated_database[lookup_key].copy()
            if time and "time" not in data:
                data["time"] = time
            return data
        else:
            # Fall back to seasonal defaults for other historical dates
            logger.warning(f"[WEATHER_MCP] No curated data for {date}, using seasonal estimate")
            return self._generate_seasonal_weather(date, location, time)

    def _generate_seasonal_weather(self, date: str, location: str, time: Optional[str] = None) -> Dict[str, Any]:
        """Generate reasonable seasonal weather for non-critical dates.

        Args:
            date: Date string
            location: Location string
            time: Optional time string

        Returns:
            Weather data dictionary
        """
        try:
            month = int(date.split("-")[1])
        except:
            month = 6

        # Seattle seasonal patterns
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
            "cloud_cover": "Overcast"
        }

        if time:
            weather_data["time"] = time

        return weather_data


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
        """Generate realistic random weather data based on location and season.

        Args:
            date: Date string (YYYY-MM-DD)
            location: Location string
            time: Optional time string (HH:MM)

        Returns:
            Weather data dictionary
        """
        import random
        import hashlib

        # Parse month for seasonal variation
        try:
            month = int(date.split("-")[1])
        except:
            month = 6

        # Create deterministic seed from date+location (same date = same weather)
        seed_str = f"{date}_{location}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
        random.seed(seed)

        # Seattle/Pacific Northwest weather patterns
        if "seattle" in location.lower() or "portland" in location.lower() or "spokane" in location.lower():
            if month in [12, 1, 2]:  # Winter - rainy, cold
                conditions = ["Light rain", "Heavy rain", "Cloudy", "Overcast", "Drizzle"]
                weights = [0.35, 0.25, 0.20, 0.15, 0.05]
                temp_range = (35, 48)
                humidity_range = (75, 92)
            elif month in [3, 4, 5]:  # Spring - mixed
                conditions = ["Light rain", "Partly cloudy", "Overcast", "Clear", "Drizzle"]
                weights = [0.30, 0.25, 0.20, 0.15, 0.10]
                temp_range = (48, 62)
                humidity_range = (60, 80)
            elif month in [6, 7, 8]:  # Summer - dry, sunny
                conditions = ["Clear", "Partly cloudy", "Sunny", "Overcast"]
                weights = [0.40, 0.35, 0.20, 0.05]
                temp_range = (65, 85)
                humidity_range = (45, 65)
            else:  # Fall - rainy again
                conditions = ["Light rain", "Overcast", "Cloudy", "Drizzle", "Clear"]
                weights = [0.30, 0.25, 0.20, 0.15, 0.10]
                temp_range = (50, 65)
                humidity_range = (65, 85)

        # Vancouver, BC - similar to Seattle but slightly cooler
        elif "vancouver" in location.lower():
            if month in [12, 1, 2]:  # Winter
                conditions = ["Light rain", "Heavy rain", "Snow", "Cloudy"]
                weights = [0.35, 0.25, 0.10, 0.30]
                temp_range = (32, 45)
                humidity_range = (75, 92)
            elif month in [3, 4, 5]:  # Spring
                conditions = ["Light rain", "Partly cloudy", "Overcast", "Clear"]
                weights = [0.35, 0.25, 0.25, 0.15]
                temp_range = (45, 58)
                humidity_range = (60, 80)
            elif month in [6, 7, 8]:  # Summer
                conditions = ["Clear", "Partly cloudy", "Sunny", "Light rain"]
                weights = [0.40, 0.30, 0.20, 0.10]
                temp_range = (60, 78)
                humidity_range = (50, 70)
            else:  # Fall
                conditions = ["Light rain", "Overcast", "Heavy rain", "Cloudy"]
                weights = [0.35, 0.30, 0.20, 0.15]
                temp_range = (48, 60)
                humidity_range = (70, 88)

        # Default (any other location) - generic moderate climate
        else:
            if month in [12, 1, 2]:  # Winter
                conditions = ["Cloudy", "Clear", "Snow", "Overcast"]
                weights = [0.35, 0.30, 0.20, 0.15]
                temp_range = (30, 45)
                humidity_range = (60, 80)
            elif month in [3, 4, 5]:  # Spring
                conditions = ["Partly cloudy", "Clear", "Light rain", "Cloudy"]
                weights = [0.35, 0.30, 0.20, 0.15]
                temp_range = (50, 65)
                humidity_range = (55, 75)
            elif month in [6, 7, 8]:  # Summer
                conditions = ["Clear", "Sunny", "Partly cloudy", "Hot"]
                weights = [0.40, 0.30, 0.25, 0.05]
                temp_range = (70, 90)
                humidity_range = (40, 65)
            else:  # Fall
                conditions = ["Partly cloudy", "Clear", "Overcast", "Light rain"]
                weights = [0.35, 0.30, 0.20, 0.15]
                temp_range = (55, 70)
                humidity_range = (55, 75)

        # Select random condition (weighted)
        condition = random.choices(conditions, weights=weights)[0]

        # Generate random temp and humidity within range
        temp = random.randint(*temp_range)
        humidity = random.randint(*humidity_range)
        wind_speed = random.randint(3, 20)

        # Cloud cover based on condition
        cloud_cover_map = {
            "Clear": "0-10%",
            "Sunny": "0-5%",
            "Partly cloudy": "30-50%",
            "Cloudy": "70-90%",
            "Overcast": "100%",
            "Light rain": "90-100%",
            "Heavy rain": "100%",
            "Drizzle": "100%",
            "Snow": "100%"
        }
        cloud_cover = cloud_cover_map.get(condition, "50%")

        weather_data = {
            "date": date,
            "location": location,
            "condition": condition,
            "temperature": temp,
            "humidity": humidity,
            "cloud_cover": cloud_cover,
            "wind_speed": wind_speed
        }

        if time:
            weather_data["time"] = time

        logger.info(f"[WEATHER_MCP] Generated random weather for {date} in {location}: {condition}, {temp}°F")

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
