"""Web MCP client wrapper for web scraping and content fetching.

This handles connection to Web MCP server for:
- Room 2: Scraping Echo's blog, social media, news archives
- Room 3: Fetching traffic safety studies, accident reconstruction data
"""

import logging
import os
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


async def connect_to_web_mcp():
    """Connect to Web MCP server (if enabled).

    Returns:
        Web MCP client or MockWebMCPClient if disabled
    """
    # Check if Web MCP is enabled
    enable_web = os.getenv("ENABLE_WEB_MCP", "false").lower() == "true"

    if not enable_web:
        logger.info("[WEB_MCP] Using mock web data (ENABLE_WEB_MCP=false)")
        return MockWebMCPClient()

    try:
        # TODO: Implement actual Web MCP connection
        # For now, return mock client
        logger.warning("[WEB_MCP] Web MCP server connection not yet implemented")
        logger.info("[WEB_MCP] Using mock data. To enable: Install Web MCP server")
        return MockWebMCPClient()

    except Exception as e:
        logger.error(f"[WEB_MCP] Failed to connect to Web MCP server: {e}")
        return MockWebMCPClient()


class MockWebMCPClient:
    """Mock Web MCP client with pre-configured memorial content.

    Provides simulated web scraping results for demo/testing.
    """

    def __init__(self):
        # Pre-configured web content database
        self.content_database = self._initialize_content()

    def _initialize_content(self) -> Dict[str, Any]:
        """Initialize mock web content for scraping."""
        return {
            # Echo's Blog
            "memorial-archive.com/echo/blog": {
                "type": "blog",
                "title": "Echo's Blog - Thoughts on Love & Life",
                "posts": [
                    {
                        "date": "2023-09-12",
                        "title": "On Loving Someone Who Works Too Hard",
                        "content": """He's brilliant. And stubborn. And he doesn't know when to stop working.

I worry about him sometimes. Will he remember to eat dinner? Did he sleep last night? Is he drinking enough water?

But I also love that passion. That drive. The way his eyes light up when he solves a problem. The way he talks about his work like it's the most fascinating thing in the world.

Note to self: Make sure he eats tonight. He forgets.

- Echo"""
                    },
                    {
                        "date": "2023-07-04",
                        "title": "Coffee Shop Memories",
                        "content": """We went back to the coffee shop where we had our first date today. It was raining, just like that first day.

He still orders the same thing: black coffee, too hot to drink. I still order the same thing: chai latte with extra foam.

Some things never change. And I'm grateful for that.

- Echo"""
                    }
                ]
            },

            # Social Media Archive
            "social-archive.com/echo.thompson/posts": {
                "type": "social_media",
                "platform": "Facebook",
                "posts": [
                    {
                        "id": "post_final",
                        "date": "2024-03-03",
                        "time": "22:15",
                        "content": "Heading out to pick up my workaholic husband from the lab. Again. 😊 Love him anyway. See you soon babe! ❤️",
                        "likes": 23,
                        "comments": [
                            {
                                "author": "Sarah M.",
                                "content": "Drive safe! Roads look bad tonight 🌧️",
                                "time": "22:17"
                            }
                        ],
                        "liked_by_player": True,
                        "liked_at": "22:16"
                    },
                    {
                        "id": "post_anniversary",
                        "date": "2023-10-15",
                        "content": "One year ago today, a nerdy engineer spilled coffee on himself trying to impress me at a coffee shop. Best accident ever. ❤️",
                        "likes": 156
                    }
                ]
            },

            # News Archive
            "seattle-times.com/archives/2024-03-03": {
                "type": "news",
                "headlines": [
                    {
                        "title": "Fatal Collision at 5th & Pine Intersection",
                        "time": "23:47 PM",
                        "content": """A fatal collision occurred at the intersection of 5th Avenue and Pine Street late Sunday evening.

Weather conditions: Heavy rain, poor visibility
Road conditions: Wet, high risk of hydroplaning

A vehicle ran a red light and collided with another vehicle at the intersection. One fatality reported. The driver of the other vehicle sustained minor injuries.

Police are investigating but preliminary reports indicate weather conditions were a significant factor. No charges have been filed at this time.

Witnesses report visibility was extremely poor due to heavy rainfall."""
                    }
                ]
            },

            # Traffic Safety Database
            "nhtsa.gov/reaction-time-studies": {
                "type": "safety_study",
                "title": "Human Reaction Time Study - Wet Road Conditions",
                "data": {
                    "average_reaction_dry": 1.5,  # seconds
                    "average_reaction_wet": 1.8,
                    "average_reaction_unexpected": 2.1,
                    "study_sample_size": 5000,
                    "conclusions": [
                        "Wet conditions increase reaction time by 20-40%",
                        "Unexpected obstacles can double reaction time",
                        "Even perfect reaction times cannot prevent all collisions"
                    ]
                }
            },

            # Accident Reconstruction
            "simulation.local/accident_reconstruction": {
                "type": "physics_simulation",
                "title": "Accident Reconstruction Report - Case #2024-0303",
                "data": {
                    "truck_speed": 48,  # mph
                    "road_coefficient_wet": 0.3,
                    "visibility": 500,  # feet
                    "player_reaction_time": 0.9,  # seconds
                    "collision_probability": 99.7,  # percent
                    "analysis": """Given the truck speed (48 mph), wet road surface coefficient (0.3),
and visibility conditions (<500ft), the collision was statistically unavoidable.

Even with a perfect reaction time of 0.0 seconds, the physics of the situation made impact inevitable.
The subject's actual reaction time of 0.9 seconds was 52% FASTER than the average driver in equivalent conditions.

CONCLUSION: No reasonable driver could have prevented this accident. The subject reacted appropriately and faster than expected. The collision was due to circumstances beyond anyone's control."""
                }
            }
        }

    async def call_tool(self, tool_name: str, arguments: dict) -> Dict[str, Any]:
        """Mock tool calling for web scraping.

        Args:
            tool_name: Name of the tool (e.g., "fetch_page", "search")
            arguments: Tool arguments

        Returns:
            Web content dictionary
        """
        if tool_name == "fetch_page":
            url = arguments.get("url", "")
            extract = arguments.get("extract")

            # Normalize URL for lookup
            url_key = url.replace("https://", "").replace("http://", "")

            if url_key in self.content_database:
                content = self.content_database[url_key]
                logger.info(f"[WEB_MCP] Fetched content from {url_key}")

                # Apply extraction filter if specified
                if extract and extract in content:
                    return {extract: content[extract]}

                return content
            else:
                logger.warning(f"[WEB_MCP] No content found for {url_key}")
                return {"error": "Content not found"}

        elif tool_name == "search":
            query = arguments.get("query", "")
            filter_type = arguments.get("filter")

            results = []

            # Simple keyword matching
            query_lower = query.lower()

            # Search blog posts
            if "blog" in query_lower or "echo" in query_lower:
                blog_key = "memorial-archive.com/echo/blog"
                if blog_key in self.content_database:
                    results.append({
                        "title": "Echo's Blog - Thoughts on Love & Life",
                        "url": f"https://{blog_key}",
                        "snippet": "He's brilliant. And stubborn. And he doesn't know when to stop working...",
                        "type": "blog"
                    })

            # Search social media
            if "social" in query_lower or "last post" in query_lower or "echo" in query_lower:
                social_key = "social-archive.com/echo.thompson/posts"
                if social_key in self.content_database:
                    results.append({
                        "title": "Echo Thompson - Social Media Archive",
                        "url": f"https://{social_key}",
                        "snippet": "Heading out to pick up my workaholic husband from the lab...",
                        "type": "social_media"
                    })

            # Search news
            if "news" in query_lower or "accident" in query_lower or "seattle" in query_lower:
                news_key = "seattle-times.com/archives/2024-03-03"
                if news_key in self.content_database:
                    results.append({
                        "title": "Seattle Times - Fatal Collision at 5th & Pine",
                        "url": f"https://{news_key}",
                        "snippet": "A fatal collision occurred... weather conditions were a significant factor",
                        "type": "news"
                    })

            logger.info(f"[WEB_MCP] Search for '{query}' returned {len(results)} results")
            return {"results": results}

        else:
            logger.warning(f"[MOCK_WEB_MCP] Unknown tool: {tool_name}")
            return {}

    async def fetch_page(self, url: str, extract: Optional[str] = None) -> Dict[str, Any]:
        """Convenience method for fetching a web page.

        Args:
            url: URL to fetch
            extract: Optional field to extract from content

        Returns:
            Web content dictionary
        """
        arguments = {"url": url}
        if extract:
            arguments["extract"] = extract

        return await self.call_tool("fetch_page", arguments)

    async def search(self, query: str, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Convenience method for searching web content.

        Args:
            query: Search query
            filter_type: Optional filter (e.g., "blog", "news")

        Returns:
            List of search results
        """
        arguments = {"query": query}
        if filter_type:
            arguments["filter"] = filter_type

        result = await self.call_tool("search", arguments)
        return result.get("results", [])
