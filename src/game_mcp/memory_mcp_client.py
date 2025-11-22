"""Memory MCP client wrapper for connecting to Memory MCP server.

This handles connection to the external Memory MCP server for cross-playthrough persistence.
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


async def connect_to_memory_mcp():
    """Connect to Memory MCP server (if enabled).

    Returns:
        Memory MCP client or None if disabled/unavailable
    """
    # Check if Memory MCP is enabled
    enable_memory = os.getenv("ENABLE_MEMORY_MCP", "false").lower() == "true"

    if not enable_memory:
        logger.info("[MEMORY_MCP] Memory persistence disabled (ENABLE_MEMORY_MCP=false)")
        return None

    try:
        # TODO: Implement actual Memory MCP connection
        # For now, return None - will implement when Memory MCP server is set up
        logger.warning("[MEMORY_MCP] Memory MCP server connection not yet implemented")
        logger.info("[MEMORY_MCP] To enable: Install Memory MCP server and configure connection")
        return None

    except Exception as e:
        logger.error(f"[MEMORY_MCP] Failed to connect to Memory MCP server: {e}")
        return None


class MockMemoryMCPClient:
    """Mock Memory MCP client for testing without actual Memory MCP server.

    This allows development/testing of memory features before Memory MCP is fully integrated.
    """

    def __init__(self):
        self.storage = {}  # In-memory storage for testing

    async def call_tool(self, tool_name: str, arguments: dict):
        """Mock tool calling."""
        if tool_name == "open_nodes":
            names = arguments.get("names", [])
            nodes = []
            for name in names:
                if name in self.storage:
                    nodes.append(self.storage[name])
            return {"nodes": nodes}  # Always return structure, even if empty

        elif tool_name == "create_entities":
            entities = arguments.get("entities", [])
            for entity in entities:
                self.storage[entity["name"]] = {
                    "name": entity["name"],
                    "entityType": entity.get("entityType", "unknown"),
                    "observations": entity.get("observations", [])
                }
            return {"success": True}

        elif tool_name == "delete_entities":
            names = arguments.get("entity_names", [])
            for name in names:
                self.storage.pop(name, None)
            return {"success": True}

        elif tool_name == "read_graph":
            return {"entities": list(self.storage.values())}

        else:
            logger.warning(f"[MOCK_MEMORY_MCP] Unknown tool: {tool_name}")
            return {}