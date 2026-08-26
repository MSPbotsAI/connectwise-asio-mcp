"""tools/list snapshot + error-envelope mapping tests.

No network calls: tool enumeration goes through FastMCP's in-process
list_tools(), and the error-code mapping is tested directly against
AsioError, independent of any real HTTP request.
"""

import json

import pytest

from connectwise_asio_mcp.api_client import AsioError
from connectwise_asio_mcp.config import Settings
from connectwise_asio_mcp.server import create_mcp_server

# Every tool this server registers, with its required (non-default) params.
# Trimmed 2026-08-26 from 25 to 15 tools: extracted the core RMM workflow
# (find company/site -> find device -> check its health/patch status) and
# dropped custom_fields (6, config/metadata management, not core monitoring),
# create_company (the only write tool — client onboarding isn't an agent
# task), get_site (redundant with get_company_sites), get_endpoint_applications
# (software-inventory audit, niche), and get_endpoint_system_state (overlapped
# with cpu/memory/disk/services and had an ambiguous "etc." in its own
# description). See git history for the removed tools' implementations.
EXPECTED_REQUIRED: dict[str, set[str]] = {
    "connectwise_asio_get_automation_tasks": set(),
    "connectwise_asio_get_companies": set(),
    "connectwise_asio_get_company": {"company_id"},
    "connectwise_asio_get_company_sites": {"company_id"},
    "connectwise_asio_get_sites": set(),
    "connectwise_asio_list_endpoints": {"category", "resource_type", "resources"},
    "connectwise_asio_get_endpoint": {"company_id", "site_id", "endpoint_id"},
    "connectwise_asio_get_endpoint_services": {"company_id", "site_id", "endpoint_id"},
    "connectwise_asio_get_endpoint_disk_usage": {"endpoint_id"},
    "connectwise_asio_get_endpoint_memory_usage": {"endpoint_id"},
    "connectwise_asio_get_endpoint_cpu_usage": {"endpoint_id"},
    "connectwise_asio_get_endpoint_heartbeat": {"resource_type", "resources"},
    "connectwise_asio_get_endpoint_patches": {"endpoint_id"},
    "connectwise_asio_get_os_patch_compliance_summary": {"resource_type", "resources"},
    "connectwise_asio_get_os_patch_details": {"resource_type", "resources"},
}

# Every remaining tool is read-only — the trim removed the only 2 write tools.
READ_ONLY_TOOLS = set(EXPECTED_REQUIRED)

IDEMPOTENT_TOOLS: set[str] = set()


@pytest.mark.asyncio
async def test_tools_list_snapshot():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert names == set(EXPECTED_REQUIRED), f"unexpected tool set: {names}"
    assert len(tools) == 15


@pytest.mark.asyncio
async def test_every_tool_required_params_and_description_bounds():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    by_name = {t.name: t for t in tools}

    for name, expected_required in EXPECTED_REQUIRED.items():
        tool = by_name[name]
        required = set(tool.inputSchema.get("required", []))
        assert required == expected_required, f"{name}: required={required}"

        description = tool.description or ""
        assert len(description) <= 500, f"{name}: description too long ({len(description)})"
        first_line = description.strip().splitlines()[0] if description.strip() else ""
        assert len(first_line) <= 100, f"{name}: first line too long: {first_line!r}"
        assert "API:" not in description, f"{name}: leaked an 'API:' implementation-detail line"


@pytest.mark.asyncio
async def test_read_only_tools_are_annotated():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    by_name = {t.name: t for t in tools}
    for name in READ_ONLY_TOOLS:
        tool = by_name[name]
        assert tool.annotations is not None
        assert tool.annotations.readOnlyHint is True, f"{name} should be readOnlyHint=True"


@pytest.mark.asyncio
async def test_idempotent_tools_are_annotated():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    by_name = {t.name: t for t in tools}
    for name in IDEMPOTENT_TOOLS:
        tool = by_name[name]
        assert tool.annotations is not None
        assert tool.annotations.idempotentHint is True, f"{name} should be idempotentHint=True"


@pytest.mark.asyncio
async def test_service_instructions_present_and_bounded():
    mcp = create_mcp_server(Settings())
    assert mcp.instructions
    assert len(mcp.instructions) <= 1500


@pytest.mark.parametrize(
    "status_code,expected_code,expected_retryable",
    [
        (0, "upstream_error", True),
        (400, "invalid_argument", False),
        (401, "unauthorized", False),
        (403, "unauthorized", False),
        (404, "not_found", False),
        (422, "invalid_argument", False),
        (429, "rate_limited", True),
        (500, "upstream_error", True),
        (503, "upstream_error", True),
    ],
)
def test_error_envelope_mapping(status_code, expected_code, expected_retryable):
    err = AsioError(status_code, "boom")
    envelope = json.loads(err.to_envelope())
    assert envelope["error"]["code"] == expected_code
    assert envelope["error"]["retryable"] is expected_retryable
    assert envelope["error"]["message"] == "boom"
