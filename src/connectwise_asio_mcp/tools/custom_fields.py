import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_get_custom_field_definitions(
        entity_type: str | None = None, origin_type: str | None = None
    ) -> str:
        """Get the list of custom field definitions for the partner (vendor-provided and partner-defined).

        API: GET /api/platform/v1/custom-field/definitions

        Args:
            entity_type: Optional filter by entity type (e.g. "company", "site", "endpoint").
            origin_type: Optional filter by definition origin.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v1/custom-field/definitions",
                params={"entityType": entity_type, "originType": origin_type},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_custom_field_definition(body: dict[str, object]) -> str:
        """Create a new custom field definition schema.

        API: POST /api/platform/v1/custom-field/definitions

        Args:
            body: Custom field definition schema — field name, data type,
                applicable entity type, and validation rules per the
                ConnectWise Asio Custom Fields Definitions API reference.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/api/platform/v1/custom-field/definitions", json_body=body)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_custom_field_definition(definition_id: str) -> str:
        """Get a custom field definition schema by ID.

        API: GET /api/platform/v1/custom-field/definitions/{definitionID}

        Args:
            definition_id: Definition ID, from connectwise_asio_get_custom_field_definitions.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/custom-field/definitions/{definition_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_custom_field_definition(
        definition_id: str, body: dict[str, object]
    ) -> str:
        """Replace a custom field definition schema by ID.

        API: PUT /api/platform/v1/custom-field/definitions/{definitionID}

        Args:
            definition_id: Definition ID to update.
            body: Full custom field definition schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v1/custom-field/definitions/{definition_id}", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_delete_custom_field_definition(definition_id: str) -> str:
        """Delete a custom field definition and all its values by ID.

        API: DELETE /api/platform/v1/custom-field/definitions/{definitionID}

        Args:
            definition_id: Definition ID to delete.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/platform/v1/custom-field/definitions/{definition_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_company_custom_fields(
        company_id: str,
        attribute_ids: str | None = None,
        with_defaults: bool | None = None,
        origin_type: str | None = None,
        owner_id: str | None = None,
    ) -> str:
        """Get custom field values for a company.

        API: GET /api/platform/v1/company/companies/{companyId}/custom-fields

        Args:
            company_id: Company ID.
            attribute_ids: Optional comma-separated list of attribute IDs to filter.
            with_defaults: Optional — include default values when true.
            origin_type: Optional filter by value origin.
            owner_id: Optional filter by owner ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v1/company/companies/{company_id}/custom-fields",
                params={
                    "attributeIDs": attribute_ids,
                    "withDefaults": with_defaults,
                    "originType": origin_type,
                    "ownerID": owner_id,
                },
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_company_custom_fields(
        company_id: str, body: dict[str, object]
    ) -> str:
        """Update multiple custom field values for a company.

        API: PUT /api/platform/v1/company/companies/{companyId}/custom-fields

        Args:
            company_id: Company ID.
            body: Custom field values keyed by definition/attribute ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v1/company/companies/{company_id}/custom-fields", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_site_custom_fields(
        site_id: str,
        attribute_ids: str | None = None,
        with_defaults: bool | None = None,
        origin_type: str | None = None,
        owner_id: str | None = None,
    ) -> str:
        """Get custom field values for a site.

        API: GET /api/platform/v1/company/sites/{siteId}/custom-fields

        Args:
            site_id: Site ID.
            attribute_ids: Optional comma-separated list of attribute IDs to filter.
            with_defaults: Optional — include default values when true.
            origin_type: Optional filter by value origin.
            owner_id: Optional filter by owner ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v1/company/sites/{site_id}/custom-fields",
                params={
                    "attributeIDs": attribute_ids,
                    "withDefaults": with_defaults,
                    "originType": origin_type,
                    "ownerID": owner_id,
                },
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_site_custom_fields(
        site_id: str, body: dict[str, object]
    ) -> str:
        """Update multiple custom field values for a site.

        API: PUT /api/platform/v1/company/sites/{siteId}/custom-fields

        Args:
            site_id: Site ID.
            body: Custom field values keyed by definition/attribute ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v1/company/sites/{site_id}/custom-fields", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_device_custom_fields(
        endpoint_id: str,
        attribute_ids: str | None = None,
        with_defaults: bool | None = None,
        origin_type: str | None = None,
        owner_id: str | None = None,
    ) -> str:
        """Get custom field values for a device (endpoint).

        API: GET /api/platform/v2/device/endpoints/{endpointID}/custom-fields

        Args:
            endpoint_id: Device/endpoint ID.
            attribute_ids: Optional comma-separated list of attribute IDs to filter.
            with_defaults: Optional — include default values when true.
            origin_type: Optional filter by value origin.
            owner_id: Optional filter by owner ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/device/endpoints/{endpoint_id}/custom-fields",
                params={
                    "attributeIDs": attribute_ids,
                    "withDefaults": with_defaults,
                    "originType": origin_type,
                    "ownerID": owner_id,
                },
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_device_custom_fields(
        endpoint_id: str, body: dict[str, object]
    ) -> str:
        """Update multiple custom field values for a device (endpoint).

        API: PUT /api/platform/v2/device/endpoints/{endpointID}/custom-fields

        Args:
            endpoint_id: Device/endpoint ID.
            body: Custom field values keyed by definition/attribute ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v2/device/endpoints/{endpoint_id}/custom-fields", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
