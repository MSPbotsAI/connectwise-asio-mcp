import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool()
    async def connectwise_asio_get_endpoint_patches(endpoint_id: str) -> str:
        """Get the list of OS patches for an endpoint.

        API: GET /api/platform/v2/patching/{endpointId}/patches

        Args:
            endpoint_id: Endpoint (device) ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/patching/{endpoint_id}/patches")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_os_patch_compliance_summary(
        resource_type: str,
        resources: list[str],
        limit: int = 50,
        cursor: int = 0,
        field: str | None = None,
    ) -> str:
        """Get bulk OS patch compliance summary for a set of resources.

        API: POST /api/platform/v2/os-patching/compliance/summary
        Requires scope: platform.ospatching.management.read

        Args:
            resource_type: Type of the resources list below (e.g. "endpoints").
            resources: List of resource IDs to summarize.
            limit: Page size (default 50).
            cursor: Pagination cursor (default 0).
            field: Optional field-selection filter.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                "/api/platform/v2/os-patching/compliance/summary",
                params={"limit": limit, "cursor": cursor, "field": field},
                json_body={"resourceType": resource_type, "resources": resources},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_os_patch_details(
        resource_type: str, resources: list[str], field: str | None = None
    ) -> str:
        """Get bulk OS patch details for a set of endpoints.

        API: POST /api/platform/v2/os-patching/patches/details
        Requires scope: platform.ospatching.management.read

        Args:
            resource_type: Type of the resources list below (e.g. "endpoints").
            resources: List of endpoint IDs to fetch patch details for.
            field: Optional field-selection filter.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                "/api/platform/v2/os-patching/patches/details",
                params={"field": field},
                json_body={"resourceType": resource_type, "resources": resources},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

