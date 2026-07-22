import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_get_policies() -> str:
        """List all policies available for the partner.

        API: GET /api/platform/v2/policy/policies
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v2/policy/policies")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_policy(policy_id: str) -> str:
        """Get a specific policy by ID.

        API: GET /api/platform/v2/policy/policies/{policyID}

        Args:
            policy_id: Policy ID, from connectwise_asio_get_policies.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/policy/policies/{policy_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_policy_categories(target_type: str | None = None) -> str:
        """Get policy categories and subcategories.

        API: GET /api/platform/v1/policy/categories

        Args:
            target_type: Optional filter by target type.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v1/policy/categories", params={"targetType": target_type}
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_policy_assignments(policy_id: str) -> str:
        """Get assignments (packages and groups) for a policy.

        API: GET /api/platform/v2/policy/policies/{policyID}/assignments

        Args:
            policy_id: Policy ID, from connectwise_asio_get_policies.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/policy/policies/{policy_id}/assignments")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_effective_policy(client_id: str, site_id: str, endpoint_id: str) -> str:
        """Get the effective policy applied to an endpoint.

        API: GET /api/platform/v2/policy/clients/{clientID}/sites/{siteID}/endpoints/{endpointID}/effective-policy

        Args:
            client_id: Client (company) ID.
            site_id: Site ID.
            endpoint_id: Endpoint (device) ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/policy/clients/{client_id}/sites/{site_id}/endpoints/{endpoint_id}/effective-policy"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_effective_policy_override(
        client_id: str, site_id: str, endpoint_id: str
    ) -> str:
        """Get the effective policy override for an endpoint.

        API: GET /api/platform/v2/policy/clients/{clientID}/sites/{siteID}/endpoints/{endpointID}/effective-policy/override

        Args:
            client_id: Client (company) ID.
            site_id: Site ID.
            endpoint_id: Endpoint (device) ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v2/policy/clients/{client_id}/sites/{site_id}/endpoints/{endpoint_id}/effective-policy/override"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_policy_groups() -> str:
        """List all policy groups for the partner.

        API: GET /api/platform/v2/policy/groups
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v2/policy/groups")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_policy_group(group_id: str) -> str:
        """Get a specific policy group by ID.

        API: GET /api/platform/v2/policy/groups/{groupID}

        Args:
            group_id: Policy group ID, from connectwise_asio_get_policy_groups.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/policy/groups/{group_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_packages() -> str:
        """List all packages available for the partner.

        API: GET /api/platform/v2/policy/packages
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v2/policy/packages")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_package(package_id: str) -> str:
        """Get package details by ID.

        API: GET /api/platform/v2/policy/packages/{packageID}

        Args:
            package_id: Package ID, from connectwise_asio_get_packages.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/policy/packages/{package_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_package_assignments(package_id: str) -> str:
        """Get assignments for a package.

        API: GET /api/platform/v2/policy/packages/{packageID}/assignments

        Args:
            package_id: Package ID, from connectwise_asio_get_packages.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/policy/packages/{package_id}/assignments")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
