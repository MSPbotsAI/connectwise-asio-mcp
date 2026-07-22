import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_upload_product_usage(usage_records: list) -> str:
        """Upload vendor product usage records for the partner (billing intake).

        API: POST /api/platform/v1/client-billing/product-usage (schema: array<UsageUpload>)

        Args:
            usage_records: List of UsageUpload objects. Required fields per
                record: sku_id, sku_name, quantity, company_or_site_id,
                company_or_site_name, usage_month. Optional: sku_category,
                sku_sub_category, product_family, unit_price, unit_of_measure,
                free_quantity, quantity_charged, region, usage_start_date,
                usage_end_date.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                "/api/platform/v1/client-billing/product-usage", json_body=usage_records
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_rate_limits() -> str:
        """Get the current API rate limit status for this token.

        API: GET /v1/rate_limits
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/v1/rate_limits")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
