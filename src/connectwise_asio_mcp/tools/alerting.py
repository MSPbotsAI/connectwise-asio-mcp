import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_create_alerts(alerts: list[dict]) -> str:
        """Create one or more alerts.

        API: POST /v2/alerts

        Args:
            alerts: List of alert objects, each with: company_id, site_id,
                endpoint_id, condition_id, alertDetails (object).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/v2/alerts", json_body=alerts)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_alerts(alerts: list[dict]) -> str:
        """Update one or more existing alerts.

        API: PUT /v2/alerts

        Args:
            alerts: List of alert objects, each with: alert_id, company_id,
                site_id, endpoint_id, condition_id, alertDetails (object).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put("/v2/alerts", json_body=alerts)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_delete_alerts(alerts: list[dict]) -> str:
        """Delete one or more alerts.

        API: DELETE /v2/alerts

        Args:
            alerts: List of alert identifiers, each with: alert_id,
                company_id, site_id, endpoint_id, condition_id.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete("/v2/alerts", json_body=alerts)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_post_incident_alerts(incidents: list[dict]) -> str:
        """Add or update alert details for one or more security incidents.

        API: POST /api/v1/incidents

        Args:
            incidents: List of incident/alert detail objects. Common fields:
                incidentId, incidentDisplayName, incidentStatus, incidentSeverity,
                alertId, alertTitle, alertCategory, alertSeverity, alertStatus,
                companyId, siteId, endpointId, vendorEndpointId,
                threatDisplayName, threatFamilyName, mitreTechniques,
                incidentCreatedDateTime, incidentLastUpdateDateTime, evidence
                (array). See the ConnectWise Asio Incidents/Alerts API
                reference for the complete field list.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/api/v1/incidents", json_body=incidents)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
