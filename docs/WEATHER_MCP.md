# Weather MCP Integration

## Overview

Echo Hearts uses a **hybrid Weather MCP client** that supports both real-world weather data and curated puzzle data.

## Architecture

### Two Client Modes

1. **MockWeatherMCPClient** (Default)
   - Curated historical data for puzzle dates
   - Seasonal defaults for other dates
   - No API key required
   - Works offline

2. **RealWeatherMCPClient** (Optional)
   - OpenWeather API integration
   - Real weather for recent dates
   - Curated data for historical puzzle dates
   - Requires free API key

## How It Works

### Initialization

```python
# In game_state.py
async def _initialize_mcp(self):
    self.weather_mcp_client = await connect_to_weather_mcp()
```

The `connect_to_weather_mcp()` function checks for `OPENWEATHER_API_KEY`:
- **If set**: Returns `RealWeatherMCPClient` (uses API)
- **If not set**: Returns `MockWeatherMCPClient` (uses mock data)

### RealWeatherMCPClient Logic

```python
async def get_historical_weather(self, date, location):
    date_obj = datetime.fromisoformat(date)
    days_ago = (datetime.now() - date_obj).days

    if days_ago > 5:
        # Historical date - use curated data
        return await self._get_curated_historical_data(date, location)
    else:
        # Recent date - fetch from OpenWeather API
        return await self._fetch_from_api(city, location)
```

**Why 5 days?**
- OpenWeather free tier only provides current + forecast data
- Historical weather API requires paid subscription ($100+/month)
- 5-day threshold allows testing with recent dates while using curated data for puzzles

### Curated Puzzle Data

Both clients share the same curated database for critical game dates:

```python
curated_database = {
    "2023-10-15_seattle": {
        "condition": "Light rain",  # Room 1 puzzle answer
        "temperature": 52,
        "humidity": 78
    },
    "2024-03-03_seattle": {
        "condition": "Heavy rain",  # Room 3 puzzle answer
        "temperature": 45,
        "visibility": 500
    }
}
```

## Why Hybrid Approach?

### Problem
- **Historical Weather APIs are expensive** ($100-500/month for real historical data)
- **Free APIs only provide current/forecast** (not past dates)
- **Game needs consistent puzzle answers** (can't have "Light rain" change to "Cloudy")

### Solution
- **Curated data for puzzles** (2023-10-15, 2024-03-03) = Narrative consistency
- **Real API for recent dates** (<5 days) = Authentic MCP integration
- **Mock fallback** = Works without API key for demos

### Benefits
- ✅ Authentic MCP architecture (real API calls when available)
- ✅ Consistent game experience (puzzle answers never change)
- ✅ No cost barrier (works perfectly in mock mode)
- ✅ Scalable (can upgrade to paid historical API later)

## Configuration

### Mock Mode (Default)

**`.env` file:**
```bash
# Leave blank or omit entirely
OPENWEATHER_API_KEY=
```

**Behavior:**
- Uses `MockWeatherMCPClient`
- Returns curated data for puzzle dates
- Returns seasonal defaults for other dates
- No network calls

### Real Mode (Optional)

**Get API Key:**
1. Go to [openweathermap.org](https://openweathermap.org/api)
2. Sign up for free account
3. Generate API key (free tier: 1000 calls/day)

**`.env` file:**
```bash
OPENWEATHER_API_KEY=your_actual_api_key_here
```

**Behavior:**
- Uses `RealWeatherMCPClient`
- Fetches real data for dates within 5 days
- Uses curated data for historical dates (>5 days)
- Makes actual HTTP requests to OpenWeather API

## Testing

### Test Mock Mode

```bash
# Remove or leave OPENWEATHER_API_KEY blank in .env
python app.py
```

In game:
1. Click Weather Station button
2. Enter date: `2023-10-15`
3. Location: `Seattle, WA`
4. Result: "Light rain" (curated puzzle answer)

Try another date:
1. Enter date: `2023-11-20`
2. Location: `Seattle, WA`
3. Result: "Overcast" (seasonal default for November)

### Test Real Mode

```bash
# Add OPENWEATHER_API_KEY to .env
python app.py
```

In game:
1. Enter **recent date** (within 5 days): Gets real API data
2. Enter `2023-10-15`: Gets curated puzzle answer
3. Check logs: `[WEATHER_MCP] Using REAL OpenWeather API`

## API Response Format

Both clients return the same format:

```python
{
    "date": "2023-10-15",
    "location": "Seattle, WA",
    "condition": "Light rain",
    "temperature": 52,
    "humidity": 78,
    "cloud_cover": "Overcast",
    "precipitation": 0.2,  # Optional
    "wind_speed": 8,        # Optional
    "visibility": 5000      # Optional (Room 3 only)
}
```

## Upgrading to Full Historical API

To use real historical data for all dates:

1. **Subscribe to OpenWeather One Call API 3.0** ($100-500/month)
2. **Update `RealWeatherMCPClient._fetch_historical_data()`:**

```python
async def _fetch_historical_data(self, date, city, location):
    # One Call API 3.0 - Historical data endpoint
    lat, lon = await self._geocode_city(city)
    timestamp = int(datetime.fromisoformat(date).timestamp())

    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine"
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": self.api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return self._parse_historical_response(data)
```

3. **Remove curated database** (optional)

## Logging

Watch console for MCP mode:

**Mock Mode:**
```
[WEATHER_MCP] Using mock weather data (set OPENWEATHER_API_KEY for real data)
[WEATHER_MCP] Retrieved curated historical data for 2023-10-15
```

**Real Mode:**
```
[WEATHER_MCP] Using REAL OpenWeather API for historical data
[WEATHER_MCP] Historical date 2023-10-15 - using curated data
[WEATHER_MCP] Recent date 2025-11-22 - fetching from OpenWeather API
[WEATHER_MCP] Successfully fetched real data for Seattle
```

## Error Handling

### API Key Invalid
```python
# Returns curated data as fallback
logger.error(f"[WEATHER_MCP] API error: 401")
return await self._get_curated_historical_data(date, location)
```

### Network Error
```python
# Falls back to curated/seasonal data
logger.error(f"[WEATHER_MCP] Failed to fetch from API: {e}")
raise  # Caught by higher-level handler
```

### Invalid Date Format
```python
# Seasonal default with current date
try:
    month = int(date.split("-")[1])
except:
    month = 6  # Default to summer
```

## MCP Tool Interface

Echo and Shadow call weather data via MCP tools:

```python
# In companion personality prompt
"""
When the terminal asks about weather, use get_historical_weather tool:
- Example: "October 15th, 2023... that date feels important. Let me check..."
- [use tool with date="2023-10-15", location="Seattle"]
- React emotionally: "It was... light rain in Seattle."
"""
```

The companions don't know if data is mock or real - they just call the tool and get results!

## Storage Impact

- **Mock Mode**: 0 KB (no external dependencies)
- **Real Mode**: +150 KB (aiohttp library)
- **Total Impact**: Minimal (<0.02% of 1GB Hugging Face Space limit)

## Performance

- **Mock Mode**: <1ms (in-memory lookup)
- **Real Mode (API)**: 200-500ms (network request)
- **Real Mode (Curated)**: <1ms (fallback to mock)

## Is This "Real" MCP?

**Yes!** Here's why:

✅ **Follows MCP Architecture:**
- Client/server pattern
- Tool-based interface
- Async operations

✅ **Authentic When Possible:**
- Real API calls for recent dates
- Proper error handling
- Network I/O

✅ **Practical Tradeoffs:**
- Historical weather APIs cost $100-500/month
- Curated puzzle data ensures consistent gameplay
- Hybrid approach balances authenticity with practicality

**Analogy:** It's like a chess AI that uses opening book (curated) for first 10 moves, then switches to real calculation. Both parts are "real AI" - one is optimized, the other is computed.

## Future Enhancements

- [ ] Add weather visualization (rain animation, cloud icons)
- [ ] Cache API responses (reduce redundant calls)
- [ ] Support multiple weather providers (AccuWeather, WeatherStack)
- [ ] Add air quality data for Room 3 (accident conditions)
- [ ] Historical weather archive scraping as backup (Weather Underground)
