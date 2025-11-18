"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream
from tap_jira_nekt.streams.projects import ProjectStream


class IssueTypeStream(JiraStream):
    name = "issue_types"
    path = "/issuetype/project"
    primary_keys = ["id"]
    records_jsonpath = "$[*]"
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

        # Add project ID filter from parent context
        if context and "project_id" in context:
            params["projectId"] = context["project_id"]

        return params

    schema = th.PropertiesList(
        th.Property("self", th.StringType),
        th.Property("id", th.StringType),
        th.Property("description", th.StringType),
        th.Property("icon_url", th.StringType),
        th.Property("name", th.StringType),
        th.Property("untranslated_name", th.StringType),
        th.Property("subtask", th.BooleanType),
        th.Property("avatar_id", th.IntegerType),
        th.Property("hierarchy_level", th.IntegerType),
        th.Property(
            "scope",
            th.ObjectType(
                th.Property("type", th.StringType),
                th.Property(
                    "project",
                    th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("key", th.StringType),
                        th.Property("name", th.StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()
