"""Stream type classes for tap-jira."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira.client import JiraStream


class IssueTypeStream(JiraStream):
    name = "issue_types"
    path = "/issuetype"
    primary_keys = ["id"]
    records_jsonpath = "$[*]"

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
