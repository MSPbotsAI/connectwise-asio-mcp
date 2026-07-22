# connectwise-asio-mcp

**ConnectWise Asio** MCP server — exposes the ConnectWise Platform APIs (the "Current API" behind ConnectWise Asio, formerly SolarWinds MSP/N-central-adjacent RMM) as MCP tools.

> **Naming note:** app.mspbots.ai calls this integration **"ConnectWise Asio"** (`sys_integration.subject_code = CWASIO`). It is a distinct product from ConnectWise Command (Continuum), ConnectWise Manage (PSA), and ConnectWise Automate — each has its own MCP server in this fleet. The underlying API is officially named **"ConnectWise Platform APIs"** in its OpenAPI spec (`developer.connectwise.com` — "REST API" doc under Products > ConnectWise Platform > Platform Vendors > APIs and Callbacks).

## Overview

This server implements the [Model Context Protocol](https://modelcontextprotocol.io/) (Streamable HTTP/SSE transport) and wraps every resource in the official ConnectWise Platform APIs OpenAPI 3.0 spec (v2.7.7, 107 operations across 24 tag categories). It follows the MSPbots **Vendor MCP Service SOP**: stateless, no stored credentials, per-request header authentication.

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

**104 tools** — full coverage of every operation in the official ConnectWise Platform APIs spec (`POST /v1/token`, the token endpoint itself, is not exposed as a tool since the gateway handles OAuth token exchange, not this server).

### Companies & Contacts (13)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_get_companies` | 列出全部公司 | 无 |
| `connectwise_asio_create_company` | 新建公司(写操作) | `body`(dict, 需含 `name`) |
| `connectwise_asio_get_company` | 按 ID 查公司 | `company_id` |
| `connectwise_asio_replace_company` | 全量替换公司(写操作) | `company_id`, `body` |
| `connectwise_asio_update_company` | JSON Patch 局部更新公司(写操作) | `company_id`, `patch_operations` |
| `connectwise_asio_get_company_sites` | 列出公司下所有站点 | `company_id` |
| `connectwise_asio_create_company_site` | 在公司下新建站点(写操作) | `company_id`, `body`(需含 `name`,`timeZone`) |
| `connectwise_asio_get_company_site` | 按 ID 查公司下站点 | `company_id`, `site_id` |
| `connectwise_asio_replace_company_site` | 全量替换站点(写操作) | `company_id`, `site_id`, `body` |
| `connectwise_asio_update_company_site` | JSON Patch 局部更新站点(写操作) | `company_id`, `site_id`, `patch_operations` |
| `connectwise_asio_get_sites` | 列出全部站点(不分公司) | 无 |
| `connectwise_asio_get_site` | 按 ID 查站点(不分公司) | `site_id` |
| `connectwise_asio_create_contact` | 新建联系人(写操作) | `body`(需含 `firstName`,`lastName`) |

### Custom Fields (11)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_get_custom_field_definitions` | 列出自定义字段定义 | `entity_type?`, `origin_type?` |
| `connectwise_asio_create_custom_field_definition` | 新建自定义字段定义(写操作) | `body` |
| `connectwise_asio_get_custom_field_definition` | 按 ID 查字段定义 | `definition_id` |
| `connectwise_asio_update_custom_field_definition` | 替换字段定义(写操作) | `definition_id`, `body` |
| `connectwise_asio_delete_custom_field_definition` | 删除字段定义(写操作) | `definition_id` |
| `connectwise_asio_get_company_custom_fields` | 查公司自定义字段值 | `company_id`, `attribute_ids?`, `with_defaults?`, `origin_type?`, `owner_id?` |
| `connectwise_asio_update_company_custom_fields` | 更新公司自定义字段值(写操作) | `company_id`, `body` |
| `connectwise_asio_get_site_custom_fields` | 查站点自定义字段值 | `site_id`, `attribute_ids?`, `with_defaults?`, `origin_type?`, `owner_id?` |
| `connectwise_asio_update_site_custom_fields` | 更新站点自定义字段值(写操作) | `site_id`, `body` |
| `connectwise_asio_get_device_custom_fields` | 查设备自定义字段值 | `endpoint_id`, `attribute_ids?`, `with_defaults?`, `origin_type?`, `owner_id?` |
| `connectwise_asio_update_device_custom_fields` | 更新设备自定义字段值(写操作) | `endpoint_id`, `body` |

### Devices & Network Devices (18)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_list_endpoints` | 按分类列出设备 | `category`("platform"/"network"/"cloud"/"all"), `resource_type`, `resources`, `limit=50`, `cursor=0`, `sort_by?`, `field?`, `filter?` |
| `connectwise_asio_get_endpoint` | 查设备详情 | `company_id`, `site_id`, `endpoint_id`, `field?` |
| `connectwise_asio_get_endpoint_services` | 查设备上运行的服务 | `company_id`, `site_id`, `endpoint_id`, `service_name?`, `field?` |
| `connectwise_asio_get_endpoint_applications` | 批量查设备已装应用 | `resource_type`, `resources`, `limit=50`, `cursor=0`, `field?`, `name?`, `version?` |
| `connectwise_asio_get_endpoint_system_state` | 查设备系统状态信息 | `endpoint_id` |
| `connectwise_asio_get_hypervisor_hosts` | 查受监控的 VMware 宿主机 | 无 |
| `connectwise_asio_get_device_id_mapping` | 查 publicID/privateID 映射 | `mapping_type`("public"/"private"), `filter` |
| `connectwise_asio_get_unique_services` | 查全部唯一服务名 | 无 |
| `connectwise_asio_get_endpoint_disk_usage` | 查设备最新磁盘使用率 | `endpoint_id` |
| `connectwise_asio_get_endpoint_memory_usage` | 查设备最新内存使用率 | `endpoint_id`, `minute?` |
| `connectwise_asio_get_endpoint_cpu_usage` | 查设备最新 CPU 使用率 | `endpoint_id` |
| `connectwise_asio_uninstall_endpoints` | ⚠️批量卸载设备代理(危险写操作) | `endpoints`, `reason?`, `feedback?` |
| `connectwise_asio_get_endpoint_heartbeat` | 查设备在线/离线状态 | `resource_type`("clients"/"sites"/"endpoints"), `resources`, `offline_lookback?`, `availability?` |
| `connectwise_asio_update_endpoint_friendly_name` | 修改设备显示名(写操作) | `company_id`, `site_id`, `endpoint_id`, `friendly_name` |
| `connectwise_asio_get_device_groups` | 列出设备分组 | 无 |
| `connectwise_asio_create_network_device` | 新建网络设备记录(写操作) | `company_id`, `site_id`, `body` |
| `connectwise_asio_update_network_device` | 更新网络设备记录(写操作) | `company_id`, `site_id`, `endpoint_id`, `body` |
| `connectwise_asio_delete_network_device` | 删除网络设备记录(写操作) | `company_id`, `site_id`, `endpoint_id`, `device_id` |

### Policy, Policy Group & Package (11)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_get_policies` | 列出全部策略 | 无 |
| `connectwise_asio_get_policy` | 按 ID 查策略 | `policy_id` |
| `connectwise_asio_get_policy_categories` | 查策略分类/子分类 | `target_type?` |
| `connectwise_asio_get_policy_assignments` | 查策略的分配情况 | `policy_id` |
| `connectwise_asio_get_effective_policy` | 查设备的生效策略 | `client_id`, `site_id`, `endpoint_id` |
| `connectwise_asio_get_effective_policy_override` | 查设备生效策略的覆盖项 | `client_id`, `site_id`, `endpoint_id` |
| `connectwise_asio_get_policy_groups` | 列出策略组 | 无 |
| `connectwise_asio_get_policy_group` | 按 ID 查策略组 | `group_id` |
| `connectwise_asio_get_packages` | 列出全部安装包 | 无 |
| `connectwise_asio_get_package` | 按 ID 查安装包 | `package_id` |
| `connectwise_asio_get_package_assignments` | 查安装包的分配情况 | `package_id` |

### Patching — OS & Third-Party (6)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_get_endpoint_patches` | 查设备补丁列表 | `endpoint_id` |
| `connectwise_asio_get_os_patch_compliance_summary` | 批量查 OS 补丁合规汇总 | `resource_type`, `resources`, `limit=50`, `cursor=0`, `field?` |
| `connectwise_asio_get_os_patch_details` | 批量查 OS 补丁详情 | `resource_type`, `resources`, `field?` |
| `connectwise_asio_get_os_patch_inventory` | 查合作伙伴补丁库存 | `field?` |
| `connectwise_asio_get_third_party_patch_compliance_summary` | 批量查第三方补丁合规汇总 | `resource_type`, `resources`, `limit=500`, `cursor=0`, `field?` |
| `connectwise_asio_get_third_party_patch_details` | 批量查第三方补丁详情 | `resource_type`, `resources`, `limit=500`, `cursor=0`, `field?` |

### Tickets (24)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_get_ticket_categories` | 列出工单分类 | 无 |
| `connectwise_asio_get_ticket_priorities` | 列出工单优先级 | 无 |
| `connectwise_asio_get_service_boards` | 列出服务看板 | `company_id?`, `site_id?`, `type_id?` |
| `connectwise_asio_get_service_board_teams` | 查看板关联团队 | `board_id` |
| `connectwise_asio_get_ticket_sources` | 列出工单来源 | 无 |
| `connectwise_asio_get_ticket_statuses` | 列出工单状态 | 无 |
| `connectwise_asio_get_ticket_tags` | 列出工单标签 | 无 |
| `connectwise_asio_create_ticket_tag` | 新建工单标签(写操作) | `name` |
| `connectwise_asio_get_ticket_tag` | 按 ID 查标签 | `tag_id` |
| `connectwise_asio_replace_ticket_tag` | 替换标签(写操作) | `tag_id`, `name` |
| `connectwise_asio_update_ticket_tag` | JSON Patch 更新标签(写操作) | `tag_id`, `patch_operations` |
| `connectwise_asio_delete_ticket_tag` | 删除标签(写操作) | `tag_id` |
| `connectwise_asio_get_ticket_counts` | 查工单计数 | 无 |
| `connectwise_asio_get_ticket_notes` | 查工单备注列表 | `ticket_id`, `detail?`, `extended_attribute_ids?`, `visibility?`, `created_by?`, `created_at_to?` |
| `connectwise_asio_create_ticket_note` | 新建工单备注(写操作) | `ticket_id`, `detail`, `visibility`, `extended_attributes?` |
| `connectwise_asio_get_ticket_note` | 按 ID 查备注 | `ticket_id`, `note_id` |
| `connectwise_asio_replace_ticket_note` | 替换备注(写操作) | `ticket_id`, `note_id`, `detail`, `visibility`, `extended_attributes?` |
| `connectwise_asio_update_ticket_note` | JSON Patch 更新备注(写操作) | `ticket_id`, `note_id`, `patch_operations` |
| `connectwise_asio_get_ticket_types` | 列出工单类型 | `entity?` |
| `connectwise_asio_get_tickets` | 多条件搜索工单 | 30+ 个可选过滤参数(见工具 docstring),如 `company_ids`, `status_names`, `created_at_from/to` 等 |
| `connectwise_asio_create_ticket` | 新建工单(写操作) | `description`, `summary`, `service_board`, `source`, `extra?`(其余字段) |
| `connectwise_asio_get_ticket` | 按 ID 查工单 | `ticket_id` |
| `connectwise_asio_replace_ticket` | 替换工单(写操作) | `ticket_id`, `description`, `summary`, `service_board`, `source`, `extra?` |
| `connectwise_asio_update_ticket` | JSON Patch 更新工单(写操作) | `ticket_id`, `patch_operations` |

### Alerting & Incidents (4)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_create_alerts` | 批量创建告警(写操作) | `alerts` |
| `connectwise_asio_update_alerts` | 批量更新告警(写操作) | `alerts` |
| `connectwise_asio_delete_alerts` | 批量删除告警(写操作) | `alerts` |
| `connectwise_asio_post_incident_alerts` | 上报/更新安全事件告警详情(写操作) | `incidents` |

### Mapping (8)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_lookup_mappings` | 按 schema 查属性映射 | `schemas`, `criteria`, `all?` |
| `connectwise_asio_get_site_endpoint_mappings` | 查站点的集成商设备映射 | `company_id`, `site_id` |
| `connectwise_asio_create_site_endpoint_mappings` | 新建/更新站点设备映射(写操作) | `company_id`, `site_id`, `mappings` |
| `connectwise_asio_replace_site_endpoint_mappings` | 全量替换站点设备映射(写操作) | `company_id`, `site_id`, `mappings` |
| `connectwise_asio_delete_site_endpoint_mappings` | 删除站点全部设备映射(写操作) | `company_id`, `site_id` |
| `connectwise_asio_delete_site_endpoint_mapping` | 删除单个设备映射(写操作) | `company_id`, `site_id`, `endpoint_id` |
| `connectwise_asio_get_partner_endpoint_mappings` | 查合作伙伴全部设备映射 | 无 |
| `connectwise_asio_get_site_mappings` | 查站点映射列表 | 无 |

### Automation (3)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_get_scripts` | 列出自动化脚本 | 无 |
| `connectwise_asio_get_shell_scripts` | 列出 Shell 脚本 | 无 |
| `connectwise_asio_get_automation_tasks` | 列出自动化任务 | 无 |

### Backup Dashboard (4)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_resolve_alarm` | 关闭备份告警(写操作) | `company_id`, `site_id`, `alarm_id`, `vendor_device_id` |
| `connectwise_asio_create_alarm_record` | 上报备份告警记录(写操作) | `company_id`, `site_id`, `alarms`, `family`, `severity`, `type` |
| `connectwise_asio_create_dr_readiness_record` | 上报灾备就绪验证记录(写操作) | `company_id`, `site_id`, `id`, `devices`, `triggered_by`, `backup_job_id?`, `backup_name?` |
| `connectwise_asio_create_backup_record` | 上报备份运行记录(写操作) | `company_id`, `site_id`, `backup_job_id`, `backup_job_name`, `devices`, `job_type`, `managed_by`, `appliance_id?`, `appliance_name?` |

### Misc (2)

| Tool | 功能 | 参数 |
|---|---|---|
| `connectwise_asio_upload_product_usage` | 上传厂商产品用量记录(计费,写操作) | `usage_records` |
| `connectwise_asio_get_rate_limits` | 查当前 API 速率限制状态 | 无 |

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

- Not yet tested against a live ConnectWise Asio account — only protocol-level verification (health check, 401 on missing token, `tools/list` returning all 104 tools) has been done so far.
- Several request bodies with deeply nested schemas (e.g. `Company`, `Contact`, `Ticket`, `NetworkDevice`) are exposed as a generic `body: dict` / `extra: dict` parameter rather than fully flattened named arguments — the docstring lists the required top-level fields, but nested object shapes should be cross-checked against the live API on first use.
- `connectwise_asio_uninstall_endpoints` is destructive (removes RMM agents) — do not call against production data without explicit confirmation for each device.
