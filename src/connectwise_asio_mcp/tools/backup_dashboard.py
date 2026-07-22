import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_resolve_alarm(
        company_id: str, site_id: str, alarm_id: str, vendor_device_id: str
    ) -> str:
        """Resolve a previously created backup alarm record.

        API: PATCH /api/backup-dashboard/companies/{companyID}/sites/{siteID}/alarms/{alarmID}

        Args:
            company_id: Company ID.
            site_id: Site ID.
            alarm_id: Alarm record ID to resolve.
            vendor_device_id: Vendor-side device ID the alarm applies to.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(
                f"/api/backup-dashboard/companies/{company_id}/sites/{site_id}/alarms/{alarm_id}",
                json_body={"vendorDeviceID": vendor_device_id},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_alarm_record(
        company_id: str, site_id: str, alarms: list, family: str, severity: str, type: str
    ) -> str:
        """Store a backup alarm record raised by the vendor.

        API: POST /api/backup-dashboard/v2/companies/{companyID}/sites/{siteID}/alarms (schema: alarmRecord)

        Args:
            company_id: Company ID.
            site_id: Site ID.
            alarms: Required list of alarm detail objects.
            family: Required alarm family/category.
            severity: Required alarm severity.
            type: Required alarm type.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                f"/api/backup-dashboard/v2/companies/{company_id}/sites/{site_id}/alarms",
                json_body={"alarms": alarms, "family": family, "severity": severity, "type": type},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_dr_readiness_record(
        company_id: str,
        site_id: str,
        id: str,
        devices: list,
        triggered_by: str,
        backup_job_id: str | None = None,
        backup_name: str | None = None,
    ) -> str:
        """Store a record corresponding to a disaster-recovery readiness verification run.

        API: POST /api/backup-dashboard/v2/companies/{companyID}/sites/{siteID}/dr-readiness (schema: drReadinessRecord)

        Args:
            company_id: Company ID.
            site_id: Site ID.
            id: Required unique record ID.
            devices: Required list of devices covered by this DR readiness run.
            triggered_by: Required — what/who triggered this run.
            backup_job_id: Optional backup job ID.
            backup_name: Optional backup name.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"id": id, "devices": devices, "triggeredBy": triggered_by}
        if backup_job_id is not None:
            body["backupJobID"] = backup_job_id
        if backup_name is not None:
            body["backupName"] = backup_name
        try:
            result = await client.post(
                f"/api/backup-dashboard/v2/companies/{company_id}/sites/{site_id}/dr-readiness",
                json_body=body,
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_backup_record(
        company_id: str,
        site_id: str,
        backup_job_id: str,
        backup_job_name: str,
        devices: list,
        job_type: str,
        managed_by: str,
        appliance_id: str | None = None,
        appliance_name: str | None = None,
    ) -> str:
        """Store a record corresponding to a backup run on a device.

        API: POST /api/backup-dashboard/v2/companies/{companyID}/sites/{siteID}/instances (schema: backupInstanceRecord)

        Args:
            company_id: Company ID.
            site_id: Site ID.
            backup_job_id: Required backup job ID.
            backup_job_name: Required backup job name.
            devices: Required list of devices covered by this backup run.
            job_type: Required backup job type.
            managed_by: Required — who/what manages this backup job.
            appliance_id: Optional backup appliance ID.
            appliance_name: Optional backup appliance name.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {
            "backupJobID": backup_job_id,
            "backupJobName": backup_job_name,
            "devices": devices,
            "jobType": job_type,
            "managedBy": managed_by,
        }
        if appliance_id is not None:
            body["applianceID"] = appliance_id
        if appliance_name is not None:
            body["applianceName"] = appliance_name
        try:
            result = await client.post(
                f"/api/backup-dashboard/v2/companies/{company_id}/sites/{site_id}/instances",
                json_body=body,
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
