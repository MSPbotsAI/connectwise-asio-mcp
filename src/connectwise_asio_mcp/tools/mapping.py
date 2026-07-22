import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_lookup_mappings(schemas: list, criteria: dict, all: bool | None = None) -> str:
        """Look up attributes for given schema IDs based on source attributes.

        API: POST /api/platform/v1/mapping/mappings/lookup (schema: LookupRequest)

        Args:
            schemas: List of SchemaLookupDef objects identifying which schemas to resolve.
            criteria: LookupCriteria object — source attributes to match against.
            all: Optional — if true, return all matches instead of the best match.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                "/api/platform/v1/mapping/mappings/lookup",
                params={"all": all},
                json_body={"schemas": schemas, "criteria": criteria},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_site_endpoint_mappings(company_id: str, site_id: str) -> str:
        """Get all integrator endpoint mappings for a company's site.

        API: GET /api/platform/v2/companies/{companyID}/sites/{siteID}/endpoint-mapping

        Args:
            company_id: Company ID.
            site_id: Site ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/companies/{company_id}/sites/{site_id}/endpoint-mapping"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_site_endpoint_mappings(
        company_id: str, site_id: str, mappings: list
    ) -> str:
        """Create or update integrator endpoint mappings for a company's site.

        API: POST /api/platform/v2/companies/{companyID}/sites/{siteID}/endpoint-mapping

        Args:
            company_id: Company ID.
            site_id: Site ID.
            mappings: List of NewEndpointMappingV2 objects, each with required
                fields: integrator_endpoint_id (string), identifiers (object),
                asset_attributes (array of EndpointMappingAttributeV2); optional
                partial_match_criteria (array).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                f"/api/platform/v2/companies/{company_id}/sites/{site_id}/endpoint-mapping",
                json_body=mappings,
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_replace_site_endpoint_mappings(
        company_id: str, site_id: str, mappings: list
    ) -> str:
        """Replace all existing integrator endpoint mappings for a company's site with new ones.

        API: PUT /api/platform/v2/companies/{companyID}/sites/{siteID}/endpoint-mapping

        Args:
            company_id: Company ID.
            site_id: Site ID.
            mappings: List of NewEndpointMappingV2 objects (see
                connectwise_asio_create_site_endpoint_mappings for the shape).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v2/companies/{company_id}/sites/{site_id}/endpoint-mapping",
                json_body=mappings,
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_delete_site_endpoint_mappings(company_id: str, site_id: str) -> str:
        """Delete all integrator endpoint mappings for a company's site.

        API: DELETE /api/platform/v2/companies/{companyID}/sites/{siteID}/endpoint-mapping

        Args:
            company_id: Company ID.
            site_id: Site ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(
                f"/api/platform/v2/companies/{company_id}/sites/{site_id}/endpoint-mapping"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_delete_site_endpoint_mapping(
        company_id: str, site_id: str, endpoint_id: str
    ) -> str:
        """Delete the integrator endpoint mapping for one specific endpoint.

        API: DELETE /api/platform/v2/companies/{companyID}/sites/{siteID}/endpoint-mapping/{endpointID}

        Args:
            company_id: Company ID.
            site_id: Site ID.
            endpoint_id: Endpoint ID whose mapping should be deleted.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(
                f"/api/platform/v2/companies/{company_id}/sites/{site_id}/endpoint-mapping/{endpoint_id}"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_partner_endpoint_mappings() -> str:
        """Get all endpoint mappings for the partner's integrator (across all sites).

        API: GET /api/platform/v2/endpoint-mapping
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v2/endpoint-mapping")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_site_mappings() -> str:
        """Get the list of site mappings for the partner's integrator.

        API: GET /api/platform/v2/site-mappings
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v2/site-mappings")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
