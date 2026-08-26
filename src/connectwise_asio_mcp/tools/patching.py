from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN

# ConnectWise Asio's Platform APIs docs are behind a login wall and don't
# publicly document a real per-page maximum for this bulk endpoint. Fall
# back to the SOP's generic ceiling rather than trusting the vendor to
# reject an unbounded value safely.
_MAX_PAGE_SIZE = 200


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_endpoint_patches(
        endpoint_id: Annotated[str, Field(min_length=1, description="Endpoint (device) ID.")],
    ) -> str:
        """Get the list of OS patches known for an endpoint."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/patching/{endpoint_id}/patches")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_os_patch_compliance_summary(
        resource_type: Annotated[
            str,
            Field(
                description=(
                    'Type of the IDs in resources. "endpoints" is confirmed to '
                    "work; whether \"companies\"/\"sites\" also work for a rollup "
                    "is unverified against the vendor's live API (docs are "
                    "behind a login wall) — use \"endpoints\" unless you've "
                    "confirmed otherwise."
                )
            ),
        ],
        resources: Annotated[
            list[str], Field(min_length=1, description="Resource IDs to summarize — must be non-empty.")
        ],
        limit: Annotated[
            int, Field(description="Page size (default 50, capped at 200).")
        ] = 50,
        cursor: Annotated[int, Field(description="Pagination cursor (default 0).")] = 0,
        field: Annotated[str | None, Field(description="Field-selection filter.")] = None,
    ) -> str:
        """Get bulk OS patch compliance summary for a set of resources.

        Requires the platform.ospatching.management.read scope on the caller's
        access token.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        limit = min(limit, _MAX_PAGE_SIZE)
        try:
            result = await client.post(
                "/api/platform/v2/os-patching/compliance/summary",
                params={"limit": limit, "cursor": cursor, "field": field},
                json_body={"resourceType": resource_type, "resources": resources},
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_os_patch_details(
        resource_type: Annotated[
            str, Field(description='Type of the IDs in resources, e.g. "endpoints".')
        ],
        resources: Annotated[
            list[str],
            Field(min_length=1, description="Endpoint IDs to fetch patch details for — must be non-empty."),
        ],
        field: Annotated[str | None, Field(description="Field-selection filter.")] = None,
    ) -> str:
        """Get bulk OS patch details for a set of endpoints.

        Requires the platform.ospatching.management.read scope on the caller's
        access token.
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
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()
