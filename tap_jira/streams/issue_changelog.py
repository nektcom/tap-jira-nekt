"""Stream type classes for tap-jira."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira.client import JiraStream

from .issues import IssueStream


class IssueChangeLogStream(JiraStream):
    name = "issue_changelog"
    path = "/issue/{issue_id}/changelog"
    parent_stream_type = IssueStream
    replication_key = "created"
    primary_keys = ["id"]
    records_jsonpath = "$[values][*]"
    state_partitioning_keys = []
    instance_name = "values"
    next_page_token_jsonpath = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("issue_id", th.StringType),
        th.Property("author", th.ObjectType(th.Property("account_id", th.StringType))),
        th.Property("created", th.DateTimeType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("field", th.StringType),
                    th.Property("fieldtype", th.StringType),
                    th.Property("field_id", th.StringType),
                    th.Property("from", th.StringType),
                    th.Property("from_string", th.StringType),
                    th.Property("to", th.StringType),
                    th.Property("to_string", th.StringType),
                ),
            ),
        ),
    ).to_dict()

    def post_process(self, row: dict, context: dict) -> dict:
        row["issue_id"] = context["issue_id"]
        return super().post_process(row, context)
