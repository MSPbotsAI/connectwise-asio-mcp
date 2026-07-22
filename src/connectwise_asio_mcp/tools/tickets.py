import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import AsioClient, AsioError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], AsioClient | None]) -> None:

    @mcp.tool()
    async def connectwise_asio_get_ticket_categories() -> str:
        """Get all ticket categories for the partner.

        API: GET /api/platform/v1/service/ticketing/categories
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/service/ticketing/categories")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_priorities() -> str:
        """Get all ticket priorities.

        API: GET /api/platform/v1/service/ticketing/priorities
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/service/ticketing/priorities")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_service_boards(
        company_id: str | None = None, site_id: str | None = None, type_id: str | None = None
    ) -> str:
        """Get all service boards available to the partner.

        API: GET /api/platform/v1/service/ticketing/service-boards

        Args:
            company_id: Optional filter by company ID.
            site_id: Optional filter by site ID.
            type_id: Optional filter by ticket type ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v1/service/ticketing/service-boards",
                params={"companyId": company_id, "siteId": site_id, "typeId": type_id},
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_service_board_teams(board_id: str) -> str:
        """Get team associations for a service board.

        API: GET /api/platform/v1/service/ticketing/service-boards/{id}/teams

        Args:
            board_id: Service board ID, from connectwise_asio_get_service_boards.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/service/ticketing/service-boards/{board_id}/teams")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_sources() -> str:
        """Get all ticket sources for the partner.

        API: GET /api/platform/v1/service/ticketing/sources
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/service/ticketing/sources")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_statuses() -> str:
        """Get all ticket statuses.

        API: GET /api/platform/v1/service/ticketing/statuses
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/service/ticketing/statuses")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_tags() -> str:
        """Get all tags available for tickets.

        API: GET /api/platform/v1/service/ticketing/tags
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/service/ticketing/tags")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_ticket_tag(name: str) -> str:
        """Create a new ticket tag.

        API: POST /api/platform/v1/service/ticketing/tags

        Args:
            name: Tag name.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/api/platform/v1/service/ticketing/tags", json_body={"name": name})
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_tag(tag_id: str) -> str:
        """Get a ticket tag by ID.

        API: GET /api/platform/v1/service/ticketing/tags/{id}

        Args:
            tag_id: Tag ID, from connectwise_asio_get_ticket_tags.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v1/service/ticketing/tags/{tag_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_replace_ticket_tag(tag_id: str, name: str) -> str:
        """Replace a ticket tag by ID.

        API: PUT /api/platform/v1/service/ticketing/tags/{id}

        Args:
            tag_id: Tag ID to replace.
            name: New tag name.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(
                f"/api/platform/v1/service/ticketing/tags/{tag_id}", json_body={"name": name}
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_ticket_tag(tag_id: str, patch_operations: list) -> str:
        """Partially update a ticket tag using JSON Patch (RFC 6902).

        API: PATCH /api/platform/v1/service/ticketing/tags/{id}

        Args:
            tag_id: Tag ID to update.
            patch_operations: List of JSON Patch operations, e.g.
                [{"op": "replace", "path": "/name", "value": "New Name"}].
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(
                f"/api/platform/v1/service/ticketing/tags/{tag_id}", json_body=patch_operations
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_delete_ticket_tag(tag_id: str) -> str:
        """Delete a ticket tag by ID.

        API: DELETE /api/platform/v1/service/ticketing/tags/{id}

        Args:
            tag_id: Tag ID to delete.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/platform/v1/service/ticketing/tags/{tag_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_counts() -> str:
        """Get ticket counts for the partner.

        API: GET /api/platform/v1/service/ticketing/ticket-counts
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/platform/v1/service/ticketing/ticket-counts")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_notes(
        ticket_id: str,
        detail: str | None = None,
        extended_attribute_ids: str | None = None,
        visibility: str | None = None,
        created_by: str | None = None,
        created_at_to: str | None = None,
    ) -> str:
        """Get notes for a service ticket.

        API: GET /api/platform/v1/service/ticketing/tickets/{id}/notes

        Args:
            ticket_id: Ticket ID.
            detail: Optional detail-level filter.
            extended_attribute_ids: Optional comma-separated extended attribute IDs.
            visibility: Optional visibility filter.
            created_by: Optional filter by creator ID.
            created_at_to: Optional upper bound on creation date (ISO 8601).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v1/service/ticketing/tickets/{ticket_id}/notes",
                params={
                    "detail": detail,
                    "extendedAttributeIds": extended_attribute_ids,
                    "visibility": visibility,
                    "createdBy": created_by,
                    "createdAtTo": created_at_to,
                },
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_ticket_note(
        ticket_id: str, detail: str, visibility: int, extended_attributes: list | None = None
    ) -> str:
        """Create a new note on a service ticket.

        API: POST /api/platform/v1/service/ticketing/tickets/{id}/notes

        Args:
            ticket_id: Ticket ID.
            detail: Note text.
            visibility: Visibility level (integer per ConnectWise Asio ticketing config).
            extended_attributes: Optional list of TicketingExtendedAttribute objects.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"detail": detail, "visibility": visibility}
        if extended_attributes is not None:
            body["extendedAttributes"] = extended_attributes
        try:
            result = await client.post(
                f"/api/platform/v1/service/ticketing/tickets/{ticket_id}/notes", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_note(ticket_id: str, note_id: str) -> str:
        """Get a specific note on a service ticket.

        API: GET /api/platform/v1/service/ticketing/tickets/{id}/notes/{noteId}

        Args:
            ticket_id: Ticket ID.
            note_id: Note ID, from connectwise_asio_get_ticket_notes.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/platform/v1/service/ticketing/tickets/{ticket_id}/notes/{note_id}"
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_replace_ticket_note(
        ticket_id: str,
        note_id: str,
        detail: str,
        visibility: int,
        extended_attributes: list | None = None,
    ) -> str:
        """Replace a note on a service ticket.

        API: PUT /api/platform/v1/service/ticketing/tickets/{id}/notes/{noteId}

        Args:
            ticket_id: Ticket ID.
            note_id: Note ID to replace.
            detail: Note text.
            visibility: Visibility level (integer per ConnectWise Asio ticketing config).
            extended_attributes: Optional list of TicketingExtendedAttribute objects.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"detail": detail, "visibility": visibility}
        if extended_attributes is not None:
            body["extendedAttributes"] = extended_attributes
        try:
            result = await client.put(
                f"/api/platform/v1/service/ticketing/tickets/{ticket_id}/notes/{note_id}", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_ticket_note(ticket_id: str, note_id: str, patch_operations: list) -> str:
        """Partially update a note on a service ticket using JSON Patch (RFC 6902).

        API: PATCH /api/platform/v1/service/ticketing/tickets/{id}/notes/{noteId}

        Args:
            ticket_id: Ticket ID.
            note_id: Note ID to update.
            patch_operations: List of JSON Patch operations.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(
                f"/api/platform/v1/service/ticketing/tickets/{ticket_id}/notes/{note_id}",
                json_body=patch_operations,
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket_types(entity: str | None = None) -> str:
        """Get all ticket types.

        API: GET /api/platform/v1/service/ticketing/types

        Args:
            entity: Optional filter by entity type.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v1/service/ticketing/types", params={"entity": entity}
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_tickets(
        page_size: int | None = None,
        page_num: int | None = None,
        sort_by: str | None = None,
        sort_dir: str | None = None,
        number: str | None = None,
        ticket_ids: str | None = None,
        summary: str | None = None,
        company_ids: str | None = None,
        site_ids: str | None = None,
        status_ids: str | None = None,
        status_names: str | None = None,
        priority_ids: str | None = None,
        priority_names: str | None = None,
        assignee_ids: str | None = None,
        assignee_team_ids: str | None = None,
        assignee_team_names: str | None = None,
        source_ids: str | None = None,
        source_names: str | None = None,
        extended_attribute_ids: str | None = None,
        type_ids: str | None = None,
        type_names: str | None = None,
        category_ids: str | None = None,
        category_names: str | None = None,
        created_by_ids: str | None = None,
        updated_by_ids: str | None = None,
        created_at_from: str | None = None,
        created_at_to: str | None = None,
        updated_at_from: str | None = None,
        updated_at_to: str | None = None,
        due_date_from: str | None = None,
        due_date_to: str | None = None,
        tag_ids: str | None = None,
        tag_names: str | None = None,
    ) -> str:
        """Search/list service tickets with extensive filtering.

        API: GET /api/platform/v2/service/ticketing/tickets

        All filter arguments are optional; most accept comma-separated ID or
        name lists. Date arguments are ISO 8601 timestamps.

        Args:
            page_size: Number of results per page.
            page_num: Page number.
            sort_by: Field to sort by.
            sort_dir: Sort direction ("asc"/"desc").
            number: Filter by ticket number.
            ticket_ids: Comma-separated ticket IDs.
            summary: Filter by summary text.
            company_ids: Comma-separated company IDs.
            site_ids: Comma-separated site IDs.
            status_ids: Comma-separated status IDs.
            status_names: Comma-separated status names.
            priority_ids: Comma-separated priority IDs.
            priority_names: Comma-separated priority names.
            assignee_ids: Comma-separated assignee IDs.
            assignee_team_ids: Comma-separated assignee team IDs.
            assignee_team_names: Comma-separated assignee team names.
            source_ids: Comma-separated source IDs.
            source_names: Comma-separated source names.
            extended_attribute_ids: Comma-separated extended attribute IDs.
            type_ids: Comma-separated type IDs.
            type_names: Comma-separated type names.
            category_ids: Comma-separated category IDs.
            category_names: Comma-separated category names.
            created_by_ids: Comma-separated creator IDs.
            updated_by_ids: Comma-separated updater IDs.
            created_at_from: Lower bound on creation date.
            created_at_to: Upper bound on creation date.
            updated_at_from: Lower bound on last-update date.
            updated_at_to: Upper bound on last-update date.
            due_date_from: Lower bound on due date.
            due_date_to: Upper bound on due date.
            tag_ids: Comma-separated tag IDs.
            tag_names: Comma-separated tag names.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/platform/v2/service/ticketing/tickets",
                params={
                    "pageSize": page_size,
                    "pageNum": page_num,
                    "sortBy": sort_by,
                    "sortDir": sort_dir,
                    "number": number,
                    "ticketIds": ticket_ids,
                    "summary": summary,
                    "companyIds": company_ids,
                    "siteIds": site_ids,
                    "statusIds": status_ids,
                    "statusNames": status_names,
                    "priorityIds": priority_ids,
                    "priorityNames": priority_names,
                    "assigneeIds": assignee_ids,
                    "assigneeTeamIds": assignee_team_ids,
                    "assigneeTeamNames": assignee_team_names,
                    "sourceIds": source_ids,
                    "sourceNames": source_names,
                    "extendedAttributeIds": extended_attribute_ids,
                    "typeIds": type_ids,
                    "typeNames": type_names,
                    "categoryIds": category_ids,
                    "categoryNames": category_names,
                    "createdByIds": created_by_ids,
                    "updatedByIds": updated_by_ids,
                    "createdAtFrom": created_at_from,
                    "createdAtTo": created_at_to,
                    "updatedAtFrom": updated_at_from,
                    "updatedAtTo": updated_at_to,
                    "dueDateFrom": due_date_from,
                    "dueDateTo": due_date_to,
                    "tagIds": tag_ids,
                    "tagNames": tag_names,
                },
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_create_ticket(
        description: str,
        summary: str,
        service_board: dict,
        source: dict,
        extra: dict | None = None,
    ) -> str:
        """Create a new service ticket.

        API: POST /api/platform/v2/service/ticketing/tickets (schema: Ticket)

        Args:
            description: Ticket description.
            summary: Ticket summary/title.
            service_board: Required — IdWithName reference, e.g. {"id": "..."} or {"name": "..."}.
            source: Required — IdWithName reference for the ticket source.
            extra: Optional additional Ticket fields to merge in — e.g. company
                (Id), site (Id), assignee (Id), assigneeTeam (IdWithName),
                priority (IdWithName), status (IdWithName), category (IdWithName),
                type (IdWithName), tags (array of IdWithName), dueDate, assets,
                extendedAttributes.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {
            "description": description,
            "summary": summary,
            "serviceBoard": service_board,
            "source": source,
        }
        if extra:
            body.update(extra)
        try:
            result = await client.post("/api/platform/v2/service/ticketing/tickets", json_body=body)
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_get_ticket(ticket_id: str) -> str:
        """Get a service ticket by ID.

        API: GET /api/platform/v2/service/ticketing/tickets/{id}

        Args:
            ticket_id: Ticket ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/platform/v2/service/ticketing/tickets/{ticket_id}")
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_replace_ticket(
        ticket_id: str,
        description: str,
        summary: str,
        service_board: dict,
        source: dict,
        extra: dict | None = None,
    ) -> str:
        """Replace (full update) a service ticket by ID.

        API: PUT /api/platform/v2/service/ticketing/tickets/{id} (schema: Ticket)

        Args:
            ticket_id: Ticket ID to replace.
            description: Ticket description.
            summary: Ticket summary/title.
            service_board: Required — IdWithName reference.
            source: Required — IdWithName reference for the ticket source.
            extra: Optional additional Ticket fields to merge in (see
                connectwise_asio_create_ticket for the full field list).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {
            "description": description,
            "summary": summary,
            "serviceBoard": service_board,
            "source": source,
        }
        if extra:
            body.update(extra)
        try:
            result = await client.put(
                f"/api/platform/v2/service/ticketing/tickets/{ticket_id}", json_body=body
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def connectwise_asio_update_ticket(ticket_id: str, patch_operations: list) -> str:
        """Partially update a service ticket using JSON Patch (RFC 6902).

        API: PATCH /api/platform/v2/service/ticketing/tickets/{id}

        Args:
            ticket_id: Ticket ID to update.
            patch_operations: List of JSON Patch operations, e.g.
                [{"op": "replace", "path": "/status", "value": {"id": "..."}}].
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(
                f"/api/platform/v2/service/ticketing/tickets/{ticket_id}", json_body=patch_operations
            )
            return json.dumps(result, indent=2)
        except AsioError as e:
            return f"Error: {e}"
