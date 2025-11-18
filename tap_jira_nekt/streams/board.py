"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream
from tap_jira_nekt.streams.projects import ProjectStream


class BoardStream(JiraStream):
    name = "boards"
    path = "/board"
    primary_keys = ["id"]
    records_jsonpath = "$[values][*]"
    instance_name = "values"
    parent_stream_type = ProjectStream
    state_partitioning_keys = []
    ignore_parent_replication_keys = True

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return URL parameters, including project filter if configured."""
        params = super().get_url_params(context, next_page_token)

        # Add project filter from parent context
        if context and "project_key" in context:
            params["projectKeyOrId"] = context["project_key"]

        return params

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

    def get_child_context(self, record: dict, context: dict | None) -> dict | None:  # noqa: ARG002
        """Return a context dictionary for child streams.

        Only scrum boards have sprints, so we only return context for those.
        """
        if record["type"] == "scrum":
            return {"board_id": record["id"]}
        return None
