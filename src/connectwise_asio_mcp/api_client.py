import uuid
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://openapi.service.itsupport247.net"


class AsioError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"ConnectWise Asio API error {status_code}: {message}")


class AsioClient:
    """Async httpx client wrapping the ConnectWise Asio (Platform APIs) REST API.

    Auth is OAuth2 Client Credentials — this server receives an
    already-obtained bearer access token per request (via the
    X-ConnectWise-Asio-Token header) and never performs the token exchange
    itself, matching how gateway-managed OAuth integrations (e.g. Microsoft
    Graph) are handled elsewhere in this MSPbots MCP fleet.

    Some endpoints document Origin/User-Agent/X-Request-ID as required
    headers (Host is sent automatically by any HTTP client). These are
    transport plumbing, not business parameters, so this client generates
    them itself rather than exposing them as tool arguments.
    """

    def __init__(self, access_token: str, base_url: str = DEFAULT_BASE_URL):
        self._token = access_token
        self._base_url = base_url.rstrip("/")

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": self._base_url,
            "User-Agent": "connectwise-asio-mcp/0.1.0",
            "X-Request-ID": str(uuid.uuid4()),
        }

    def _clean_params(self, params: dict | None) -> dict:
        if not params:
            return {}
        return {k: v for k, v in params.items() if v is not None}

    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json_body: Any = None,
    ) -> Any:
        target = f"{self._base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.request(
                    method,
                    target,
                    headers=self._headers(),
                    params=self._clean_params(params),
                    json=json_body,
                )
        except httpx.RequestError as e:
            raise AsioError(0, f"Could not reach {target!r}: {e or type(e).__name__}") from None

        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except ValueError:
                detail = resp.text
            raise AsioError(resp.status_code, str(detail)[:500])

        if not resp.content:
            return None
        try:
            return resp.json()
        except ValueError:
            return {"raw_response": resp.text}

    async def get(self, path: str, params: dict | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, params: dict | None = None, json_body: Any = None) -> Any:
        return await self.request("POST", path, params=params, json_body=json_body)

    async def put(self, path: str, params: dict | None = None, json_body: Any = None) -> Any:
        return await self.request("PUT", path, params=params, json_body=json_body)

    async def patch(self, path: str, params: dict | None = None, json_body: Any = None) -> Any:
        return await self.request("PATCH", path, params=params, json_body=json_body)

    async def delete(self, path: str, params: dict | None = None, json_body: Any = None) -> Any:
        return await self.request("DELETE", path, params=params, json_body=json_body)
