"""Stream type classes for tap-jira."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream


class BoardStream(JiraStream):
    name = "boards"
    path = "/board"
    primary_keys = ["id"]
    records_jsonpath = "$[values][*]"
    instance_name = "values"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("self", th.StringType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("project_id", th.IntegerType),
                th.Property("display_name", th.StringType),
                th.Property("project_name", th.StringType),
                th.Property("project_key", th.StringType),
                th.Property("project_type_key", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Return the base URL for the API requests."""
        domain = self.config["domain"]
        return f"https://{domain}:443/rest/agile/1.0"

    def get_child_context(self, record: dict, context: dict | None) -> dict:  # noqa: ARG002
        """Return a context dictionary for child streams."""
        if record["type"] == "scrum":
            return {"board_id": record["id"]}
