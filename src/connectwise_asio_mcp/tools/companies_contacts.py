import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:
    @mcp.tool()
    async def connectwise_asio_get_companies() -> str:
        """List all companies (clients) for the partner.

        API: GET /api/platform/v1/company/companies
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/company/companies")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_company(body: dict[str, object]) -> str:
        """Create a new company (client).

        API: POST /api/platform/v1/company/companies (schema: CompanyCreateRequest)

        Args:
            body: Required field: name (string). Optional: description,
                friendlyName, industryCode, acquiredDate, account (ReferenceID),
                activityStatus (ReferenceID), corpContainer (ReferenceID),
                ownershipType (ReferenceID), externalIds (IdMappingCompanies),
                primarySite (SiteCreateRequest — see connectwise_asio_create_company_site
                for its shape).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/api/platform/v1/company/companies", json_body=body)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_company(company_id: str) -> str:
        """Get a company by ID.

        API: GET /api/platform/v1/company/companies/{companyId}

        Args:
            company_id: Company ID, from connectwise_asio_get_companies.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/company/companies/{company_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_company_sites(company_id: str) -> str:
        """List all sites for a company.

        API: GET /api/platform/v1/company/companies/{companyId}/sites

        Args:
            company_id: Company ID, from connectwise_asio_get_companies.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/company/companies/{company_id}/sites")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_sites() -> str:
        """List all sites for the partner (across all companies).

        API: GET /api/platform/v1/company/sites
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/company/sites")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_site(site_id: str) -> str:
        """Get a site by ID (partner-wide, not scoped to a company).

        API: GET /api/platform/v1/company/sites/{siteId}

        Args:
            site_id: Site ID, from connectwise_asio_get_sites.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/company/sites/{site_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

