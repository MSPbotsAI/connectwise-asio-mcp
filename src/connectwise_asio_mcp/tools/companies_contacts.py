from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_companies() -> str:
        """List all companies (clients) for the partner."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/company/companies")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_company(
        company_id: Annotated[
            str,
            Field(min_length=1, description="Company ID, from connectwise_asio_get_companies."),
        ],
    ) -> str:
        """Get a single company by ID."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/company/companies/{company_id}")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_company_sites(
        company_id: Annotated[
            str,
            Field(min_length=1, description="Company ID, from connectwise_asio_get_companies."),
        ],
    ) -> str:
        """List all sites belonging to a company."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/company/companies/{company_id}/sites")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_sites() -> str:
        """List all sites for the partner, across every company."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/company/sites")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

