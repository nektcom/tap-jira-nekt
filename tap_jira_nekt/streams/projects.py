"""Stream type classes for tap-jira."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream


class ProjectStream(JiraStream):
    name = "projects"
    path = "/project/search"
    primary_keys = ["id"]
    records_jsonpath = "$.values[*]"
    instance_name = "values"

    schema = th.PropertiesList(
        th.Property("expand", th.StringType),
        th.Property("self", th.StringType),
        th.Property("id", th.StringType),
        th.Property("key", th.StringType),
        th.Property("name", th.StringType),
        th.Property(
            "avatar_urls",
            th.ObjectType(
                th.Property("48x48", th.StringType),
                th.Property("24x24", th.StringType),
                th.Property("16x16", th.StringType),
                th.Property("32x32", th.StringType),
            ),
        ),
        th.Property("project_type_key", th.StringType),
        th.Property("simplified", th.BooleanType),
        th.Property("style", th.StringType),
        th.Property("is_private", th.BooleanType),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property("property_key", th.StringType),
            ),
        ),
        th.Property("entity_id", th.StringType),
        th.Property("uuid", th.StringType),
        th.Property(
            "project_category",
            th.ObjectType(
                th.Property("self", th.StringType),
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property(
            "insight",
            th.ObjectType(
                th.Property("total_issue_count", th.IntegerType),
                th.Property("last_issue_update_time", th.StringType),
            ),
        ),
    ).to_dict()
