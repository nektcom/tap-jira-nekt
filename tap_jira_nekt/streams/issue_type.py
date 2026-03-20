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
        th.Property("self", th.StringType, description="URL of the resource."),
        th.Property("id", th.StringType, description="Unique identifier of the record."),
        th.Property("description", th.StringType, description="Description of the record."),
        th.Property("icon_url", th.StringType, description="URL of the icon."),
        th.Property("name", th.StringType, description="Name of the record."),
        th.Property("untranslated_name", th.StringType, description="Untranslated name of the record."),
        th.Property("subtask", th.BooleanType, description="Subtask of the record."),
        th.Property("avatar_id", th.IntegerType, description="Identifier of the associated avatar."),
        th.Property("hierarchy_level", th.IntegerType, description="Hierarchy level of the record."),
        th.Property(
            "scope",
            th.ObjectType(
                th.Property("type", th.StringType, description="Type classification of the record."),
                th.Property(
                    "project",
                    th.ObjectType(
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                        th.Property("key", th.StringType, description="Unique key of the record."),
                        th.Property("name", th.StringType, description="Name of the record."),
                    ),
                
                    description="Project of the record."),
            ),
        
            description="Scope of the record."),
    ).to_dict()
