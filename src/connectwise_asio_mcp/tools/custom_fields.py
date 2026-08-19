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
    async def connectwise_asio_get_custom_field_definitions(
        entity_type: Annotated[
            str | None,
            Field(description='Filter by entity type, e.g. "company", "site", "endpoint".'),
        ] = None,
        origin_type: Annotated[
            str | None, Field(description="Filter by definition origin.")
        ] = None,
    ) -> str:
        """List custom field definitions for the partner (vendor-provided and partner-defined)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v1/custom-field/definitions",
                params={"entityType": entity_type, "originType": origin_type},
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_custom_field_definition(
        definition_id: Annotated[
            str,
            Field(
                description="Definition ID, from connectwise_asio_get_custom_field_definitions."
            ),
        ],
    ) -> str:
        """Get a single custom field definition's schema by ID."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/custom-field/definitions/{definition_id}")
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_company_custom_fields(
        company_id: Annotated[str, Field(description="Company ID.")],
        attribute_ids: Annotated[
            str | None, Field(description="Comma-separated attribute IDs to filter to.")
        ] = None,
        with_defaults: Annotated[
            bool | None, Field(description="Include default values when true.")
        ] = None,
        origin_type: Annotated[str | None, Field(description="Filter by value origin.")] = None,
        owner_id: Annotated[str | None, Field(description="Filter by owner ID.")] = None,
    ) -> str:
        """Get custom field values set on a company."""
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
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def connectwise_asio_update_company_custom_fields(
        company_id: Annotated[str, Field(description="Company ID.")],
        body: Annotated[
            dict[str, object],
            Field(description="Custom field values to set, keyed by definition/attribute ID."),
        ],
    ) -> str:
        """Overwrite one or more custom field values for a company."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v1/company/companies/{company_id}/custom-fields", json_body=body
            )
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_site_custom_fields(
        site_id: Annotated[str, Field(description="Site ID.")],
        attribute_ids: Annotated[
            str | None, Field(description="Comma-separated attribute IDs to filter to.")
        ] = None,
        with_defaults: Annotated[
            bool | None, Field(description="Include default values when true.")
        ] = None,
        origin_type: Annotated[str | None, Field(description="Filter by value origin.")] = None,
        owner_id: Annotated[str | None, Field(description="Filter by owner ID.")] = None,
    ) -> str:
        """Get custom field values set on a site."""
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
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def connectwise_asio_get_device_custom_fields(
        endpoint_id: Annotated[str, Field(description="Device/endpoint ID.")],
        attribute_ids: Annotated[
            str | None, Field(description="Comma-separated attribute IDs to filter to.")
        ] = None,
        with_defaults: Annotated[
            bool | None, Field(description="Include default values when true.")
        ] = None,
        origin_type: Annotated[str | None, Field(description="Filter by value origin.")] = None,
        owner_id: Annotated[str | None, Field(description="Filter by owner ID.")] = None,
    ) -> str:
        """Get custom field values set on a device (endpoint)."""
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
            return dump_json_capped(result)
        except AsioError as e:
            return e.to_envelope()
