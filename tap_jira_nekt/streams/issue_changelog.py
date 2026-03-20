"""Stream type classes for tap-jira."""

from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream

from .issues import IssueStream


class IssueChangeLogStream(JiraStream):
    name = "issue_changelog"
    path = "/issue/{issue_id}/changelog"
    parent_stream_type = IssueStream
    state_partitioning_keys = []
    replication_key = "created"
    primary_keys = ["id"]
    records_jsonpath = "$[values][*]"

    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="Unique identifier of the record."),
        th.Property("issue_id", th.StringType, description="Identifier of the associated issue."),
        th.Property("author", th.ObjectType(th.Property("account_id", th.StringType, description="Identifier of the associated account.")), description="Author of the record."),
        th.Property("created", th.DateTimeType, description="Timestamp when the record was created."),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("field", th.StringType, description="Field of the record."),
                    th.Property("fieldtype", th.StringType, description="Fieldtype of the record."),
                    th.Property("field_id", th.StringType, description="Identifier of the associated field."),
                    th.Property("from", th.StringType, description="From of the record."),
                    th.Property("from_string", th.StringType, description="From string of the record."),
                    th.Property("to", th.StringType, description="To of the record."),
                    th.Property("to_string", th.StringType, description="To string of the record."),
                ),
            ),
        
            description="Items of the record."),
    ).to_dict()

    def post_process(self, row: dict, context: dict) -> dict:
        row["issue_id"] = context["issue_id"]
        return super().post_process(row, context)
