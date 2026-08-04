import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool()
    async def connectwise_asio_get_automation_tasks() -> str:
        """Get all automation tasks for the partner.

        API: GET /api/platform/v1/automation/tasks
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/automation/tasks")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
