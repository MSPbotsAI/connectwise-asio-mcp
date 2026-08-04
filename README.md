# connectwise-asio-mcp

**ConnectWise Asio** MCP server — exposes the ConnectWise Platform APIs (the "Current API" behind ConnectWise Asio, formerly SolarWinds MSP/N-central-adjacent RMM) as MCP tools.

> **Naming note:** app.mspbots.ai calls this integration **"ConnectWise Asio"** (`sys_integration.subject_code = CWASIO`). It is a distinct product from ConnectWise Command (Continuum), ConnectWise Manage (PSA), and ConnectWise Automate — each has its own MCP server in this fleet. The underlying API is officially named **"ConnectWise Platform APIs"** in its OpenAPI spec (`developer.connectwise.com` — "REST API" doc under Products > ConnectWise Platform > Platform Vendors > APIs and Callbacks).

## Overview

This server implements the [Model Context Protocol](https://modelcontextprotocol.io/) (Streamable HTTP/SSE transport) and wraps the ConnectWise Platform APIs — **25 tools** across 5 categories (`devices`, `companies_contacts`, `custom_fields`, `patching`, `automation`), trimmed down to MSPbots' actually-configured 23 endpoints plus minimal core CRUD (see Tool List below; originally a full-API build of 107 operations across 24 tag categories). It follows the MSPbots **Vendor MCP Service SOP**: stateless, no stored credentials, per-request header authentication.

The underlying API authenticates via **OAuth2 Client Credentials**. This server does not perform the token exchange itself — it receives an already-obtained bearer access token per request (matching how other OAuth-flow integrations, e.g. Microsoft Graph, are handled in this MSPbots MCP fleet: the gateway mints/refreshes the token from `client_id`/`client_secret`/`scope`, and only the resulting token reaches this server).

## Quick Start

### Docker (recommended)

```bash
docker compose up --build
```

The server starts on `http://localhost:8080`.

### Local (uv)

```bash
uv sync
python -m connectwise_asio_mcp
```

## Health Check

```bash
curl http://localhost:8080/health
# {"status": "ok", "service": "connectwise-asio-mcp", "transport": "http"}
```

No token is required for the health endpoint.

## 授权参数说明 (Authentication)

Every request to `/mcp` must include the following HTTP headers:

| Header | 类型 | 是否必填 | 默认值 | 枚举值 | 字段描述 | Example |
|---|---|---|---|---|---|---|
| `X-ConnectWise-Asio-Token` | string | 必填 | 无 | 无(自由文本) | OAuth2 bearer access token,由调用方(Agent Platform / 上游网关)通过 `POST /v1/token`(client_credentials grant,需 client_id + client_secret + scope)预先换取并负责刷新。本服务从不接触 client_id/client_secret,只转发已获取的 token。 | `X-ConnectWise-Asio-Token: <access_token>` |
| `X-ConnectWise-Asio-Base-Url` | string | 可选 | `CONNECTWISE_ASIO_BASE_URL` 环境变量(默认 `https://openapi.service.itsupport247.net`) | `https://openapi.service.itsupport247.net`(NA)、`https://openapi.service.euplatform.connectwise.com`(EU)、`https://openapi.service.auplatform.connectwise.com`(AU) | ConnectWise Asio 按账号所属地区分 3 个独立服务器(Client ID 前缀 0e30=NA/0e31=EU/0e32=AU 可判断地区);不带该 header 时用环境变量默认值,网关同时服务多地区租户时按请求覆盖。 | `X-ConnectWise-Asio-Base-Url: https://openapi.service.euplatform.connectwise.com` |

Missing `X-ConnectWise-Asio-Token` returns `401 Unauthorized`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MCP_HTTP_PORT` | `8080` | Listening port |
| `MCP_HTTP_HOST` | `0.0.0.0` | Listening host |
| `CONNECTWISE_ASIO_BASE_URL` | `https://openapi.service.itsupport247.net` | Default regional server; override per-request with `X-ConnectWise-Asio-Base-Url` |

## MCP Endpoint

```
POST http://localhost:8080/mcp
```

Connect your MCP client with:
- Transport: `http` (Streamable HTTP / SSE)
- Headers: `X-ConnectWise-Asio-Token: <access_token>` (required), `X-ConnectWise-Asio-Base-Url: <base_url>` (optional)

## Tool List

**25 tools**, trimmed down from an original 104-tool full-API build (2026-08-04). MSPbots' own stored integration config for this vendor calls 23 endpoints across 6 underlying resource categories (devices/endpoints, companies, sites, custom fields, patching, automation) — every one of those 23 configured endpoints (including separate v1/v2 path variants, which collapse onto the same tool here) maps to a tool kept below, marked with the endpoint name it corresponds to. Everything else from the original 104-tool build (Tickets — the single largest category at 24 tools, Policy/Policy Group/Package, Mapping, Alerting & Incidents, Backup Dashboard, Misc — 6 categories, ~79 tools) was removed as unused by MSPbots. If a removed category is needed later, the vendor's OpenAPI spec (linked below) still documents its exact operations and they can be re-added the same way the kept tools were generated.

**Known gap carried over from the original build**: MSPbots configured two endpoints — "ConnectWise Asio Suspension" (`GET /v2/alerting/suspensions`) and "ConnectWise Asio Suspension Details" (`GET /v2/alerting/suspensions/{ruleid}`) — that have **no corresponding tool** in this server at all (the original 104-tool build's `alerting` category only ever implemented create/update/delete/post-incident operations, never a GET-suspension read). This predates the trim and was not introduced by it; flagged here since it's now more visible with the smaller tool count. See Known Gaps below.

### Companies & Contacts (6)

| Tool | Description | Params |
|---|---|---|
| `connectwise_asio_create_company` | Create a new company (client). | body |
| `connectwise_asio_get_companies` | List all companies (clients) for the partner. | none |
| `connectwise_asio_get_company` | Get a company by ID. | company_id |
| `connectwise_asio_get_company_sites` | List all sites for a company. | company_id |
| `connectwise_asio_get_site` | Get a site by ID (partner-wide, not scoped to a company). | site_id |
| `connectwise_asio_get_sites` | List all sites for the partner (across all companies). | none |

### Custom Fields (6)

| Tool | Description | Params |
|---|---|---|
| `connectwise_asio_get_company_custom_fields` | Get custom field values for a company. | company_id, attribute_ids?, with_defaults?, origin_type?, owner_id? |
| `connectwise_asio_get_custom_field_definition` | Get a custom field definition schema by ID. | definition_id |
| `connectwise_asio_get_custom_field_definitions` | Get the list of custom field definitions for the partner (vendor-provided and partner-defined). | entity_type?, origin_type? |
| `connectwise_asio_get_device_custom_fields` | Get custom field values for a device (endpoint). | endpoint_id, attribute_ids?, with_defaults?, origin_type?, owner_id? |
| `connectwise_asio_get_site_custom_fields` | Get custom field values for a site. | site_id, attribute_ids?, with_defaults?, origin_type?, owner_id? |
| `connectwise_asio_update_company_custom_fields` | Update multiple custom field values for a company. | company_id, body |

### Devices & Endpoints (9)

| Tool | Description | Params |
|---|---|---|
| `connectwise_asio_get_endpoint` | Get full details of a specific endpoint (device). | company_id, site_id, endpoint_id, field? |
| `connectwise_asio_get_endpoint_applications` | Get installed application details for a set of endpoints. | resource_type, resources, limit, cursor, field?, name?, version? |
| `connectwise_asio_get_endpoint_cpu_usage` | Get the latest CPU usage for an endpoint. | endpoint_id |
| `connectwise_asio_get_endpoint_disk_usage` | Get the latest disk usage for an endpoint. | endpoint_id |
| `connectwise_asio_get_endpoint_heartbeat` | Get online/offline availability information for devices. | resource_type, resources, offline_lookback?, availability? |
| `connectwise_asio_get_endpoint_memory_usage` | Get the latest memory usage for an endpoint. | endpoint_id, minute? |
| `connectwise_asio_get_endpoint_services` | Get service (Windows service / daemon) details for an endpoint. | company_id, site_id, endpoint_id, service_name?, field? |
| `connectwise_asio_get_endpoint_system_state` | Get system state information (running processes, services, etc.) of an endpoint. | endpoint_id |
| `connectwise_asio_list_endpoints` | List devices (endpoints) for a given category, scoped to specific resources. | category, resource_type, resources, limit, cursor, sort_by?, field?, filter? |

### Patching (3)

| Tool | Description | Params |
|---|---|---|
| `connectwise_asio_get_endpoint_patches` | Get the list of OS patches for an endpoint. | endpoint_id |
| `connectwise_asio_get_os_patch_compliance_summary` | Get bulk OS patch compliance summary for a set of resources. | resource_type, resources, limit, cursor, field? |
| `connectwise_asio_get_os_patch_details` | Get bulk OS patch details for a set of endpoints. | resource_type, resources, field? |

### Automation (1)

| Tool | Description | Params |
|---|---|---|
| `connectwise_asio_get_automation_tasks` | Get all automation tasks for the partner. | none |


## 测试示例 (Test Example)

Get a company list, then its sites:

```json
{
  "method": "tools/call",
  "params": { "name": "connectwise_asio_get_companies", "arguments": {} }
}
```

Equivalent `curl` against the running server (streamable HTTP MCP endpoint):

```bash
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "X-ConnectWise-Asio-Token: <access_token>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": { "name": "connectwise_asio_get_companies", "arguments": {} }
  }'
```

A parameterized call:

```json
{
  "method": "tools/call",
  "params": {
    "name": "connectwise_asio_get_endpoint_cpu_usage",
    "arguments": { "endpoint_id": "abc-123" }
  }
}
```

## API Reference

- Official docs (ConnectWise Developer Network — requires login): Products > ConnectWise Platform > Platform Vendors > APIs and Callbacks > REST API
- Base URLs: NA `https://openapi.service.itsupport247.net`, EU `https://openapi.service.euplatform.connectwise.com`, AU `https://openapi.service.auplatform.connectwise.com`

## Known Gaps / Not Yet Verified

- **Trimmed from 104 to 25 tools on 2026-08-04.** The original build covered
  the full ConnectWise Platform APIs spec per an earlier scope decision. A
  later scope decision cut this back to MSPbots' actually-used categories —
  see the Tool List section above for the exact endpoint→tool mapping and
  the full list of the 6 removed categories (~79 tools, including the
  24-tool `tickets` category, the single largest one in the original
  build). If a removed category is needed later, the vendor's OpenAPI spec
  (linked below) still documents its exact operations and they can be
  re-added the same way the kept tools were generated.
- **MSPbots' configured "Suspension"/"Suspension Details" endpoints have no
  corresponding tool** — this gap predates the trim (the original 104-tool
  build's `alerting` category never implemented a GET-suspension read
  operation, only create/update/delete/post-incident) and was not
  introduced by it. If suspension data is actually needed, this would need
  to be added from the vendor's OpenAPI spec.
- Not yet tested against a live ConnectWise Asio account — only
  protocol-level verification (health check, 401 on missing token,
  `tools/list` returning all 25 tools) has been done so far.
- `connectwise_asio_update_company_custom_fields` and
  `connectwise_asio_create_company` take a generic `body: dict` parameter
  rather than fully flattened named arguments — the docstring lists the
  required top-level fields, but nested object shapes should be
  cross-checked against the live API on first use.
