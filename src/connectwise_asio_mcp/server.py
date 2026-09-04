import contextvars
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .api_client import AsioClient
from .config import Settings

# Per-request credential isolation via contextvars.
# GatewayTokenMiddleware sets this before the MCP handler runs.
# Python asyncio copies context per task, so concurrent SSE connections are isolated.
# Value is (access_token, base_url_override) — base_url_override is None unless
# the caller sent X-ConnectWise-Asio-Base-Url (3 regional servers per tenant).
_gateway_creds_var: contextvars.ContextVar[tuple[str, str | None] | None] = contextvars.ContextVar(
    "connectwise_asio_gateway_creds", default=None
)


def get_client_from_context(settings: Settings) -> AsioClient | None:
    """Resolve the active AsioClient for the current request context."""
    creds = _gateway_creds_var.get()
    if not creds:
        return None
    token, base_url_override = creds
    return AsioClient(token, base_url_override or settings.connectwise_asio_base_url)


class GatewayTokenMiddleware:
    """ASGI middleware.

    Reads X-ConnectWise-Asio-Token (required) and X-ConnectWise-Asio-Base-Url
    (optional, per-tenant regional override) from request headers and stores
    them in the contextvar. Returns 401 if the token header is missing on
    /mcp requests.
    """

    def __init__(self, app: ASGIApp, settings: Settings):
        self.app = app
        self.settings = settings

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if not path.startswith("/mcp"):
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        token = request.headers.get("x-connectwise-asio-token")
        if not token:
            response = JSONResponse(
                {
                    "error": "Missing credentials",
                    "message": (
                        "This server requires the X-ConnectWise-Asio-Token header "
                        "containing a valid OAuth2 bearer access token"
                    ),
                    "required_headers": ["X-ConnectWise-Asio-Token"],
                    "optional_headers": ["X-ConnectWise-Asio-Base-Url"],
                },
                status_code=401,
            )
            await response(scope, receive, send)
            return

        base_url_override = request.headers.get("x-connectwise-asio-base-url")
        ctx_token = _gateway_creds_var.set((token, base_url_override))
        try:
            await self.app(scope, receive, send)
        finally:
            _gateway_creds_var.reset(ctx_token)


def create_mcp_server(settings: Settings) -> FastMCP:
    """Build the FastMCP server instance and register all ConnectWise Asio tools."""
    # DNS-rebinding protection is a browser-oriented safeguard that rejects
    # non-localhost Host headers with 421. Disable it so the server works
    # correctly behind a reverse proxy or docker network.
    mcp = FastMCP(
        name="connectwise-asio-mcp",
        instructions=(
            "ConnectWise Asio (formerly ITSupport247) is an MSP RMM/automation "
            "platform: partners manage client companies, each company's sites, "
            "the endpoint devices (workstations/servers) at those sites, OS "
            "patching compliance for those endpoints, and automation task "
            "workflows. The 4 tool domains: companies_contacts (companies and "
            "their sites), devices (fleet inventory plus endpoint telemetry — "
            "CPU/memory/disk/services/heartbeat), patching (per-endpoint patch "
            "lists and bulk OS-patch compliance/detail summaries), and "
            "automation (scheduled automation tasks). Typical flow: "
            "connectwise_asio_get_companies -> connectwise_asio_get_company_sites "
            "-> connectwise_asio_list_endpoints to discover devices and their "
            "company_id/site_id/endpoint_id together — connectwise_asio_get_endpoint "
            "and connectwise_asio_get_endpoint_services need all 3 IDs already "
            "known and cannot themselves be used to discover a device. All "
            "tools here are read-only."
        ),
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        stateless_http=True,
        json_response=True,
    )

    client_factory: Callable[[], AsioClient | None] = lambda: get_client_from_context(settings)

    from .tools import (
        automation,
        companies_contacts,
        devices,
        patching,
    )

    companies_contacts.register(mcp, client_factory)
    devices.register(mcp, client_factory)
    patching.register(mcp, client_factory)
    automation.register(mcp, client_factory)

    return mcp
