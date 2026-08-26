from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN

# ConnectWise Asio's Platform APIs docs are behind a login wall and don't
# publicly document a real per-page maximum for these bulk/list endpoints.
# Fall back to the SOP's generic ceiling rather than trusting the vendor to
# reject an unbounded value safely.
_MAX_PAGE_SIZE = 200


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_list_endpoints(
        category: Annotated[
            str, Field(description='One of "platform", "network", "cloud", "all".')
        ],
        resource_type: Annotated[
            str, Field(description='Type of the IDs in resources, e.g. "companies", "sites".')
        ],
        resources: Annotated[
            list[str],
            Field(
                min_length=1,
                description="Resource IDs (companies/sites) to fetch endpoints for. Must be non-empty — resolve at least one company/site ID first (e.g. via connectwise_asio_get_companies), don't call this with an unscoped/empty list.",
            ),
        ],
        limit: Annotated[
            int, Field(description="Page size (default 50, capped at 200).")
        ] = 50,
        cursor: Annotated[int, Field(description="Pagination cursor (default 0).")] = 0,
        sort_by: Annotated[str | None, Field(description="Sort field.")] = None,
        field: Annotated[str | None, Field(description="Field-selection filter.")] = None,
        filter: Annotated[str | None, Field(description="Filter expression.")] = None,
    ) -> str:
        """List devices (endpoints) for a category, scoped to specific resources."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        limit = min(limit, _MAX_PAGE_SIZE)
        try:
            result = await client.post(
                f"/api/platform/v2/device/categories/{category}/endpoints",
                params={
                    "limit": limit,
                    "cursor": cursor,
                    "sortBy": sort_by,
                    "field": field,
                    "filter": filter,
                },
                json_body={"resourceType": resource_type, "resources": resources},
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint(
        company_id: Annotated[str, Field(min_length=1, description="Company ID.")],
        site_id: Annotated[str, Field(min_length=1, description="Site ID.")],
        endpoint_id: Annotated[str, Field(min_length=1, description="Endpoint (device) ID.")],
        field: Annotated[str | None, Field(description="Field-selection filter.")] = None,
    ) -> str:
        """Get full details of a specific endpoint (device). Needs
        company_id/site_id/endpoint_id already known — use
        connectwise_asio_list_endpoints first to discover a device and
        get all 3 IDs together; this tool can't discover one on its own.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/companies/{company_id}/sites/{site_id}"
                f"/endpoints/{endpoint_id}",
                params={"field": field},
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint_services(
        company_id: Annotated[str, Field(min_length=1, description="Company ID.")],
        site_id: Annotated[str, Field(min_length=1, description="Site ID.")],
        endpoint_id: Annotated[str, Field(min_length=1, description="Endpoint (device) ID.")],
        service_name: Annotated[
            str | None, Field(description="Filter to a specific service name.")
        ] = None,
        field: Annotated[str | None, Field(description="Field-selection filter.")] = None,
    ) -> str:
        """Get service (Windows service / daemon) details for an endpoint.
        Needs company_id/site_id/endpoint_id already known — use
        connectwise_asio_list_endpoints first to discover a device.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/companies/{company_id}/sites/{site_id}"
                f"/endpoints/{endpoint_id}/services",
                params={"serviceName": service_name, "field": field},
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint_disk_usage(
        endpoint_id: Annotated[str, Field(min_length=1, description="Endpoint (device) ID.")],
    ) -> str:
        """Get the latest disk usage for an endpoint."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/device/endpoints/{endpoint_id}/disk-usage")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint_memory_usage(
        endpoint_id: Annotated[str, Field(min_length=1, description="Endpoint (device) ID.")],
        minute: Annotated[
            int | None, Field(description="Minutes of history to look back.")
        ] = None,
    ) -> str:
        """Get the latest memory usage for an endpoint."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/endpoints/{endpoint_id}/memory-usage",
                params={"minute": minute},
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint_cpu_usage(
        endpoint_id: Annotated[str, Field(min_length=1, description="Endpoint (device) ID.")],
    ) -> str:
        """Get the latest CPU usage for an endpoint."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/device/endpoints/{endpoint_id}/cpu-usage")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint_heartbeat(
        resource_type: Annotated[
            str, Field(description='One of "clients", "sites", "endpoints".')
        ],
        resources: Annotated[
            list[str],
            Field(
                min_length=1,
                description="Resource IDs matching resource_type — same array shape as every other bulk tool here (list_endpoints, get_os_patch_compliance_summary, get_os_patch_details).",
            ),
        ],
        offline_lookback: Annotated[
            str | None, Field(description="Lookback window for offline detection.")
        ] = None,
        availability: Annotated[
            str | None, Field(description='Filter — "true" or "false".')
        ] = None,
    ) -> str:
        """Get online/offline availability for a set of devices."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v2/device/endpoints/heartbeat",
                params={
                    "resourceType": resource_type,
                    "resources": ",".join(resources),
                    "offlineLookback": offline_lookback,
                    "availability": availability,
                },
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()
