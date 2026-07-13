"""Stream type classes for tap-jira."""

from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Mapping

import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.pagination import JSONPathPaginator

from tap_jira_nekt.client import JiraStream


class IssueStream(JiraStream):
    name = "issues"
    path = "/search/jql"
    primary_keys = ["id"]
    replication_key = "updated"
    records_jsonpath = "$[issues][*]"

    # Fallback lower bound for the "updated" JQL clause when there's no bookmark yet.
    # Jira's /search/jql endpoint rejects fully unbounded queries, so this keeps the
    # request "bounded" while still matching every record.
    MIN_UPDATED_TIMESTAMP = "1900/01/01 00:00"

    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="Unique identifier of the record."),
        th.Property("self", th.StringType, description="URL of the resource."),
        th.Property("key", th.StringType, description="Unique key of the record."),
        th.Property("fields", th.StringType, description="Fields of the record as a JSON string."),
        th.Property("created", th.DateTimeType, description="Timestamp when the record was created."),
        th.Property("updated", th.DateTimeType, description="Timestamp when the record was last updated."),
    ).to_dict()

    def get_new_paginator(self) -> JSONPathPaginator:
        return JSONPathPaginator(jsonpath="$.nextPageToken")

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of query parameters."""
        params: dict = {}
        params["maxResults"] = 100
        params["fields"] = "*all"

        jql: list[str] = []

        if next_page_token:
            params["nextPageToken"] = next_page_token

        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        starting_timestamp = self.get_starting_timestamp(context)
        # Jira's /search/jql endpoint rejects fully unbounded queries, so fall back to a
        # fixed minimal date when there's no bookmark yet. This matches every record, same
        # as omitting the clause, while keeping the request "bounded".
        lower_bound = starting_timestamp.strftime("%Y/%m/%d %H:%M") if starting_timestamp else self.MIN_UPDATED_TIMESTAMP
        jql.append(f"updated>='{lower_bound}'")

        # Add project filter if configured
        project_keys = self.config.get("project_keys")
        if project_keys:
            project_filter = " OR ".join([f'project = "{key}"' for key in project_keys])
            jql.append(f"({project_filter})")

        if base_jql := self.config.get("stream_options", {}).get("issues", {}).get("jql"):
            jql.append(f"({base_jql})")

        if jql:
            params["jql"] = " and ".join(jql)

        return params

    def validate_response(self, response: requests.Response) -> None:
        return super().validate_response(response)

    def post_process(self, row: dict[str, Any], context: Mapping[str, Any] | None = None) -> dict | None:
        row.pop("expand", None)
        fields = row.get("fields") or {}
        row["created"] = fields.get("created")
        row["updated"] = fields.get("updated")
        row["fields"] = json.dumps(fields, default=self._json_default)
        return super().post_process(row, context)

    @staticmethod
    def _json_default(obj: Any) -> Any:  # noqa: ANN401
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    def get_child_context(self, record: dict, context: dict | None) -> dict:  # noqa: ARG002
        """Return a context dictionary for child streams."""
        return {"issue_id": record["id"]}
