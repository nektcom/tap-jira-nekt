"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from nekt_singer_sdk.custom_logger import user_logger

from tap_jira_nekt.client import JiraStream


class ProjectStream(JiraStream):
    name = "projects"
    path = "/project/search"
    primary_keys = ["id"]
    records_jsonpath = "$.values[*]"

    def get_records(
        self,
        context: dict | None,
    ) -> t.Iterable[dict[str, t.Any]]:
        """Get records, making separate API calls per project key."""
        project_keys = self.config.get("project_keys")

        if not project_keys:
            yield from super().get_records(context)
            return

        for project_key in project_keys:
            self.records_jsonpath = "$"
            url = self.url_base + f"/project/{project_key}"

            try:
                # Make a direct request for this single project
                response = self.request_decorator(self._request)(
                    self.build_prepared_request(
                        method="GET",
                        url=url,
                        headers=self.http_headers,
                    ),
                    context,
                )
                project_data = response.json()
                yield self.post_process(project_data, context)

            except Exception as e:  # noqa: BLE001
                user_logger.warning(f"Failed to fetch project '{project_key}': {e}")

    def get_child_context(
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
    ) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "project_id": record["id"],
            "project_key": record["key"],
        }

    schema = th.PropertiesList(
        th.Property("expand", th.StringType, description="Expandable fields included in the response."),
        th.Property("self", th.StringType, description="URL of the resource."),
        th.Property("id", th.StringType, description="Unique identifier of the record."),
        th.Property("key", th.StringType, description="Unique key of the record."),
        th.Property("name", th.StringType, description="Name of the record."),
        th.Property(
            "avatar_urls",
            th.ObjectType(
                th.Property("48x48", th.StringType, description="48x48 of the record."),
                th.Property("24x24", th.StringType, description="24x24 of the record."),
                th.Property("16x16", th.StringType, description="16x16 of the record."),
                th.Property("32x32", th.StringType, description="32x32 of the record."),
            ),
        
            description="URLs related to the avatar."),
        th.Property("project_type_key", th.StringType, description="Project type key of the record."),
        th.Property("simplified", th.BooleanType, description="Simplified of the record."),
        th.Property("style", th.StringType, description="Style of the record."),
        th.Property("is_private", th.BooleanType, description="Indicates whether the record is private."),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property("property_key", th.StringType, description="Property key of the record."),
            ),
        
            description="Properties of the record."),
        th.Property("entity_id", th.StringType, description="Identifier of the associated entity."),
        th.Property("uuid", th.StringType, description="Uuid of the record."),
        th.Property(
            "project_category",
            th.ObjectType(
                th.Property("self", th.StringType, description="URL of the resource."),
                th.Property("id", th.StringType, description="Unique identifier of the record."),
                th.Property("name", th.StringType, description="Name of the record."),
                th.Property("description", th.StringType, description="Description of the record."),
            ),
        
            description="Project category of the record."),
        th.Property(
            "insight",
            th.ObjectType(
                th.Property("total_issue_count", th.IntegerType, description="Total issue count of the record."),
                th.Property("last_issue_update_time", th.StringType, description="Date or time value for last issue update time."),
            ),
        
            description="Insight of the record."),
    ).to_dict()
