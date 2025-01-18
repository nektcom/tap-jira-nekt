"""Stream type classes for tap-jira."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream


class FieldsStream(JiraStream):
    name = "fields"
    path = "/field/search"
    records_jsonpath = "$.values[*]"
    primary_keys = ["id"]
    instance_name = "values"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("key", th.StringType),
        th.Property("name", th.StringType),
        th.Property("untranslated_name", th.StringType),
        th.Property("custom", th.BooleanType),
        th.Property("orderable", th.BooleanType),
        th.Property("navigable", th.BooleanType),
        th.Property("searchable", th.BooleanType),
        th.Property("clause_names", th.ArrayType(th.StringType)),
        th.Property(
            "scope",
            th.ObjectType(
                th.Property("type", th.StringType),
                th.Property(
                    "project",
                    th.ObjectType(
                        th.Property("id", th.StringType),
                    ),
                ),
            ),
        ),
        th.Property(
            "schema",
            th.ObjectType(
                th.Property("type", th.StringType),
                th.Property("system", th.StringType),
                th.Property("items", th.StringType),
                th.Property("custom", th.StringType),
                th.Property("custom_id", th.IntegerType),
                th.Property(
                    "configuration",
                    th.ObjectType(
                        th.Property("custom_renderer", th.BooleanType),
                        th.Property("read_only", th.BooleanType),
                        th.Property("environment", th.StringType),
                    ),
                ),
            ),
        ),
    ).to_dict()
