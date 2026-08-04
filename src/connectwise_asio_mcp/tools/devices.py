import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool()
    async def connectwise_asio_list_endpoints(
        category: str,
        resource_type: str,
        resources: list[str],
        limit: int = 50,
        cursor: int = 0,
        sort_by: str | None = None,
        field: str | None = None,
        filter: str | None = None,
    ) -> str:
        """List devices (endpoints) for a given category, scoped to specific resources.

        API: POST /api/platform/v2/device/categories/{category}/endpoints

        Args:
            category: One of "platform", "network", "cloud", "all".
            resource_type: Type of the resources list below (e.g. "companies", "sites").
            resources: List of resource IDs (companies/sites) to fetch endpoints for.
            limit: Page size (default 50).
            cursor: Pagination cursor (default 0).
            sort_by: Optional sort field.
            field: Optional field-selection filter.
            filter: Optional filter expression.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                f"/api/platform/v2/device/categories/{category}/endpoints",
                params={"limit": limit, "cursor": cursor, "sortBy": sort_by, "field": field, "filter": filter},
                json_body={"resourceType": resource_type, "resources": resources},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint(
        company_id: str, site_id: str, endpoint_id: str, field: str | None = None
    ) -> str:
        """Get full details of a specific endpoint (device).

        API: GET /api/platform/v2/device/companies/{companyID}/sites/{siteID}/endpoints/{endpointID}

        Args:
            company_id: Company ID.
            site_id: Site ID.
            endpoint_id: Endpoint (device) ID.
            field: Optional field-selection filter.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/companies/{company_id}/sites/{site_id}/endpoints/{endpoint_id}",
                params={"field": field},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_services(
        company_id: str,
        site_id: str,
        endpoint_id: str,
        service_name: str | None = None,
        field: str | None = None,
    ) -> str:
        """Get service (Windows service / daemon) details for an endpoint.

        API: GET /api/platform/v2/device/companies/{companyID}/sites/{siteID}/endpoints/{endpointID}/services

        Args:
            company_id: Company ID.
            site_id: Site ID.
            endpoint_id: Endpoint (device) ID.
            service_name: Optional filter to a specific service name.
            field: Optional field-selection filter.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/companies/{company_id}/sites/{site_id}/endpoints/{endpoint_id}/services",
                params={"serviceName": service_name, "field": field},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_applications(
        resource_type: str,
        resources: list[str],
        limit: int = 50,
        cursor: int = 0,
        field: str | None = None,
        name: str | None = None,
        version: str | None = None,
    ) -> str:
        """Get installed application details for a set of endpoints.

        API: POST /api/platform/v2/device/endpoints/applications

        Args:
            resource_type: Type of the resources list below (e.g. "endpoints").
            resources: List of endpoint IDs to fetch application data for.
            limit: Page size (default 50).
            cursor: Pagination cursor (default 0).
            field: Optional field-selection filter.
            name: Optional filter by application name.
            version: Optional filter by application version.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                "/api/platform/v2/device/endpoints/applications",
                params={"limit": limit, "cursor": cursor, "field": field, "name": name, "version": version},
                json_body={"resourceType": resource_type, "resources": resources},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_system_state(endpoint_id: str) -> str:
        """Get system state information (running processes, services, etc.) of an endpoint.

        API: GET /api/platform/v2/device/endpoints/{endpointId}/system-state-info

        Args:
            endpoint_id: Endpoint (device) ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/device/endpoints/{endpoint_id}/system-state-info")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_disk_usage(endpoint_id: str) -> str:
        """Get the latest disk usage for an endpoint.

        API: GET /api/platform/v2/device/endpoints/{endpointId}/disk-usage

        Args:
            endpoint_id: Endpoint (device) ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/device/endpoints/{endpoint_id}/disk-usage")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_memory_usage(endpoint_id: str, minute: int | None = None) -> str:
        """Get the latest memory usage for an endpoint.

        API: GET /api/platform/v2/device/endpoints/{endpointId}/memory-usage

        Args:
            endpoint_id: Endpoint (device) ID.
            minute: Optional — minutes of history to look back.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/endpoints/{endpoint_id}/memory-usage",
                params={"minute": minute},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_cpu_usage(endpoint_id: str) -> str:
        """Get the latest CPU usage for an endpoint.

        API: GET /api/platform/v2/device/endpoints/{endpointId}/cpu-usage

        Args:
            endpoint_id: Endpoint (device) ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/device/endpoints/{endpoint_id}/cpu-usage")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_endpoint_heartbeat(
        resource_type: str,
        resources: str,
        offline_lookback: str | None = None,
        availability: str | None = None,
    ) -> str:
        """Get online/offline availability information for devices.

        API: GET /api/platform/v2/device/endpoints/heartbeat

        Args:
            resource_type: One of "clients", "sites", "endpoints".
            resources: Comma-separated list of resource IDs matching resource_type.
            offline_lookback: Optional lookback window for offline detection.
            availability: Optional filter — "true" or "false".
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v2/device/endpoints/heartbeat",
                params={
                    "resourceType": resource_type,
                    "resources": resources,
                    "offlineLookback": offline_lookback,
                    "availability": availability,
                },
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

