"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream
from tap_jira_nekt.streams import BoardStream


class SprintStream(JiraStream):
    name = "sprints"
    parent_stream_type = BoardStream
    state_partitioning_keys = []
    path = "/board/{board_id}/sprint"
    replication_key = "id"
    records_jsonpath = "$[values][*]"
    instance_name = "values"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, description="Unique identifier of the record."),
        th.Property("self", th.StringType, description="URL of the resource."),
        th.Property("state", th.StringType, description="Current state of the record."),
        th.Property("name", th.StringType, description="Name of the record."),
        th.Property("start_date", th.DateTimeType, description="Date or time value for start date."),
        th.Property("end_date", th.DateTimeType, description="Date or time value for end date."),
        th.Property("complete_date", th.DateTimeType, description="Date or time value for complete date."),
        th.Property("origin_board_id", th.IntegerType, description="Identifier of the associated origin board."),
        th.Property("goal", th.StringType, description="Goal defined for the record."),
        th.Property("board_id", th.IntegerType, description="Identifier of the associated board."),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Return the base URL for the API requests."""
        domain = self.config["domain"]
        return f"https://{domain}:443/rest/agile/1.0"

    def post_process(self, row: dict, context: dict | None) -> dict:
        """Post-process the record before it is returned."""
        if context:
            row["board_id"] = context["board_id"]
        return super().post_process(row, context)
