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
    async def connectwise_asio_replace_company(company_id: str, body: dict[str, object]) -> str:
        """Replace (full update) a company by ID.

        API: PUT /api/platform/v1/company/companies/{companyId} (schema: CompanyUpdateRequest)

        Args:
            company_id: Company ID to replace.
            body: Required field: name (string). Optional: description,
                friendlyName, industryCode, acquiredDate, parentCompanyId,
                account/activityStatus/corpContainer/ownershipType (ReferenceID).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/platform/v1/company/companies/{company_id}", json_body=body)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_company(company_id: str, patch_operations: list[dict]) -> str:
        """Partially update a company using JSON Patch (RFC 6902).

        API: PATCH /api/platform/v1/company/companies/{companyId}

        Args:
            company_id: Company ID to update.
            patch_operations: List of JSON Patch operations, e.g.
                [{"op": "replace", "path": "/description", "value": "New description"}].
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(
                f"/api/platform/v1/company/companies/{company_id}", json_body=patch_operations
            )
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
    async def connectwise_asio_create_company_site(
        company_id: str, body: dict[str, object]
    ) -> str:
        """Create a new site under a company.

        API: POST /api/platform/v1/company/companies/{companyId}/sites (schema: SiteCreateRequest)

        Args:
            company_id: Company ID to create the site under.
            body: Required fields: name (string), timeZone (string). Optional:
                description, friendlyName, industryCode, activeFlag,
                physicalAddressFlag, primaryFlag, primaryAddress, primaryEmail,
                primaryPhoneNumber, primarySocialMedia, type, externalIds.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                f"/api/platform/v1/company/companies/{company_id}/sites", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_company_site(company_id: str, site_id: str) -> str:
        """Get a specific site for a company.

        API: GET /api/platform/v1/company/companies/{companyId}/sites/{siteId}

        Args:
            company_id: Company ID.
            site_id: Site ID, from connectwise_asio_get_company_sites.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v1/company/companies/{company_id}/sites/{site_id}"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_replace_company_site(
        company_id: str, site_id: str, body: dict[str, object]
    ) -> str:
        """Replace (full update) a company's site by ID.

        API: PUT /api/platform/v1/company/companies/{companyId}/sites/{siteId} (schema: Site)

        Args:
            company_id: Company ID.
            site_id: Site ID to replace.
            body: Full Site object — common fields: name, description,
                friendlyName, activeFlag, industryCode, timeZone,
                primaryAddress, primaryContact, primaryEmail, primaryFlag,
                primaryPhoneNumber, primarySocialMedia, type, externalIds.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v1/company/companies/{company_id}/sites/{site_id}", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_company_site(
        company_id: str, site_id: str, patch_operations: list[dict]
    ) -> str:
        """Partially update a company's site using JSON Patch (RFC 6902).

        API: PATCH /api/platform/v1/company/companies/{companyId}/sites/{siteId}

        Args:
            company_id: Company ID.
            site_id: Site ID to update.
            patch_operations: List of JSON Patch operations, e.g.
                [{"op": "replace", "path": "/timeZone", "value": "America/New_York"}].
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(
                f"/api/platform/v1/company/companies/{company_id}/sites/{site_id}",
                json_body=patch_operations,
            )
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

    @mcp.tool()
    async def connectwise_asio_create_contact(body: dict[str, object]) -> str:
        """Create a new contact.

        API: POST /api/platform/v1/contact/contacts (schema: ContactCreateRequest)

        Args:
            body: Required fields: firstName (string), lastName (string).
                Optional: description, salutation, title, activeFlag, type
                (ReferenceID), company (ContactCompanyReference), addresses
                (array of AddressCreateRequest), emails (array of
                EmailCreateRequest), phoneNumbers (array of
                PhoneNumberCreateRequest), faxNumbers (array of
                FaxNumberCreateRequest), socialMedias (array of
                SocialMediaCreateRequest), externalIds (IdMappingContacts).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/api/platform/v1/contact/contacts", json_body=body)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
