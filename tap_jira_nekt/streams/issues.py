"""Stream type classes for tap-jira."""

from __future__ import annotations

from typing import Any, Mapping

import requests  # JSON Schema typing helpers
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.pagination import JSONPathPaginator

from tap_jira_nekt.client import JiraStream


class IssueStream(JiraStream):
    name = "issues"
    path = "/search/jql"
    primary_keys = ["id"]
    replication_key = "updated"
    records_jsonpath = "$[issues][*]"

    # TODO: Add custom fields and description
    schema = th.PropertiesList(
        th.Property("expand", th.StringType),
        th.Property("id", th.StringType),
        th.Property("self", th.StringType),
        th.Property("key", th.StringType),
        th.Property(
            "fields",
            th.ObjectType(
                th.Property("description", th.StringType),
                th.Property("created", th.DateTimeType),
                th.Property("updated", th.DateTimeType),
                th.Property(
                    "status_category",
                    th.ObjectType(
                        th.Property("color_name", th.StringType),
                        th.Property("id", th.IntegerType),
                        th.Property("key", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("self", th.StringType),
                    ),
                ),
                th.Property("statuscategorychangedate", th.StringType),
                th.Property(
                    "issuetype",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("id", th.StringType),
                        th.Property("description", th.StringType),
                        th.Property("icon_url", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("subtask", th.BooleanType),
                        th.Property("avatar_id", th.IntegerType),
                        th.Property("entity_id", th.StringType),
                        th.Property("hierarchy_level", th.IntegerType),
                    ),
                ),
                th.Property(
                    "parent",
                    th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("key", th.StringType),
                        th.Property("self", th.StringType),
                        th.Property(
                            "fields",
                            th.ObjectType(
                                th.Property("summary", th.StringType),
                                th.Property("created", th.DateTimeType),
                                th.Property("updated", th.DateTimeType),
                                th.Property(
                                    "status",
                                    th.ObjectType(
                                        th.Property("description", th.StringType),
                                        th.Property("icon_url", th.StringType),
                                        th.Property("id", th.StringType),
                                        th.Property("name", th.StringType),
                                        th.Property("self", th.StringType),
                                        th.Property(
                                            "status_category",
                                            th.ObjectType(
                                                th.Property("color_name", th.StringType),
                                                th.Property("id", th.IntegerType),
                                                th.Property("key", th.StringType),
                                                th.Property("name", th.StringType),
                                                th.Property("self", th.StringType),
                                            ),
                                        ),
                                    ),
                                ),
                                th.Property(
                                    "priority",
                                    th.ObjectType(
                                        th.Property("self", th.StringType),
                                        th.Property("icon_url", th.StringType),
                                        th.Property("name", th.StringType),
                                        th.Property("id", th.StringType),
                                    ),
                                ),
                                th.Property(
                                    "issuetype",
                                    th.ObjectType(
                                        th.Property("self", th.StringType),
                                        th.Property("id", th.StringType),
                                        th.Property("description", th.StringType),
                                        th.Property("icon_url", th.StringType),
                                        th.Property("name", th.StringType),
                                        th.Property("subtask", th.BooleanType),
                                        th.Property("avatar_id", th.IntegerType),
                                        th.Property("entity_id", th.StringType),
                                        th.Property("hierarchy_level", th.IntegerType),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                th.Property("timespent", th.IntegerType),
                th.Property(
                    "project",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("id", th.StringType),
                        th.Property("key", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("project_type_key", th.StringType),
                        th.Property("simplified", th.BooleanType),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType),
                                th.Property("24x24", th.StringType),
                                th.Property("16x16", th.StringType),
                                th.Property("32x32", th.StringType),
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "fix_versions",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("archived", th.BooleanType),
                            th.Property("name", th.StringType),
                            th.Property("released", th.BooleanType),
                            th.Property("self", th.StringType),
                        ),
                    ),
                ),
                th.Property("aggregatetimespent", th.IntegerType),
                th.Property(
                    "resolution",
                    th.ObjectType(
                        th.Property("description", th.StringType),
                        th.Property("id", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("self", th.StringType),
                    ),
                ),
                th.Property("resolutiondate", th.StringType),
                th.Property("workratio", th.IntegerType),
                th.Property(
                    "watches",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("watch_count", th.IntegerType),
                        th.Property("is_watching", th.BooleanType),
                    ),
                ),
                th.Property("issuerestriction", th.StringType),
                th.Property("last_viewed", th.StringType),
                th.Property(
                    "priority",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("icon_url", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("id", th.StringType),
                    ),
                ),
                th.Property("labels", th.ArrayType(th.StringType)),
                th.Property("timeestimate", th.IntegerType),
                th.Property("aggregatetimeoriginalestimate", th.IntegerType),
                th.Property("versions", th.ArrayType(th.StringType)),
                th.Property(
                    "issuelinks",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property(
                                "outward_issue",
                                th.ObjectType(
                                    th.Property(
                                        "fields",
                                        th.ObjectType(
                                            th.Property(
                                                "issuetype",
                                                th.ObjectType(
                                                    th.Property("avatar_id", th.IntegerType),
                                                    th.Property("description", th.StringType),
                                                    th.Property("entity_id", th.StringType),
                                                    th.Property(
                                                        "hierarchy_level",
                                                        th.IntegerType,
                                                    ),
                                                    th.Property("icon_url", th.StringType),
                                                    th.Property("id", th.StringType),
                                                    th.Property("name", th.StringType),
                                                    th.Property("self", th.StringType),
                                                    th.Property("subtask", th.BooleanType),
                                                ),
                                            ),
                                            th.Property(
                                                "priority",
                                                th.ObjectType(
                                                    th.Property("icon_url", th.StringType),
                                                    th.Property("id", th.StringType),
                                                    th.Property("name", th.StringType),
                                                    th.Property("self", th.StringType),
                                                ),
                                            ),
                                            th.Property(
                                                "status",
                                                th.ObjectType(
                                                    th.Property("description", th.StringType),
                                                    th.Property("icon_url", th.StringType),
                                                    th.Property("id", th.StringType),
                                                    th.Property("name", th.StringType),
                                                    th.Property("self", th.StringType),
                                                    th.Property(
                                                        "status_category",
                                                        th.ObjectType(
                                                            th.Property(
                                                                "color_name",
                                                                th.StringType,
                                                            ),
                                                            th.Property("id", th.IntegerType),
                                                            th.Property("key", th.StringType),
                                                            th.Property(
                                                                "name",
                                                                th.StringType,
                                                            ),
                                                            th.Property(
                                                                "self",
                                                                th.StringType,
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            th.Property("summary", th.StringType),
                                        ),
                                    ),
                                    th.Property("id", th.StringType),
                                    th.Property("key", th.StringType),
                                    th.Property("self", th.StringType),
                                ),
                            ),
                            th.Property(
                                "inward_issue",
                                th.ObjectType(
                                    th.Property(
                                        "fields",
                                        th.ObjectType(
                                            th.Property(
                                                "issuetype",
                                                th.ObjectType(
                                                    th.Property("avatar_id", th.IntegerType),
                                                    th.Property("description", th.StringType),
                                                    th.Property("entity_id", th.StringType),
                                                    th.Property(
                                                        "hierarchy_level",
                                                        th.IntegerType,
                                                    ),
                                                    th.Property("icon_url", th.StringType),
                                                    th.Property("id", th.StringType),
                                                    th.Property("name", th.StringType),
                                                    th.Property("self", th.StringType),
                                                    th.Property("subtask", th.BooleanType),
                                                ),
                                            ),
                                            th.Property(
                                                "priority",
                                                th.ObjectType(
                                                    th.Property("icon_url", th.StringType),
                                                    th.Property("id", th.StringType),
                                                    th.Property("name", th.StringType),
                                                    th.Property("self", th.StringType),
                                                ),
                                            ),
                                            th.Property(
                                                "status",
                                                th.ObjectType(
                                                    th.Property("description", th.StringType),
                                                    th.Property("icon_url", th.StringType),
                                                    th.Property("id", th.StringType),
                                                    th.Property("name", th.StringType),
                                                    th.Property("self", th.StringType),
                                                    th.Property(
                                                        "statusCategory",
                                                        th.ObjectType(
                                                            th.Property(
                                                                "color_name",
                                                                th.StringType,
                                                            ),
                                                            th.Property("id", th.IntegerType),
                                                            th.Property("key", th.StringType),
                                                            th.Property(
                                                                "name",
                                                                th.StringType,
                                                            ),
                                                            th.Property(
                                                                "self",
                                                                th.StringType,
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            th.Property("summary", th.StringType),
                                        ),
                                    ),
                                    th.Property("id", th.StringType),
                                    th.Property("key", th.StringType),
                                    th.Property("self", th.StringType),
                                ),
                            ),
                            th.Property("self", th.StringType),
                            th.Property(
                                "type",
                                th.ObjectType(
                                    th.Property("id", th.StringType),
                                    th.Property("inward", th.StringType),
                                    th.Property("name", th.StringType),
                                    th.Property("outward", th.StringType),
                                    th.Property("self", th.StringType),
                                ),
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "assignee",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("account_id", th.StringType),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType),
                                th.Property("24x24", th.StringType),
                                th.Property("16x16", th.StringType),
                                th.Property("32x32", th.StringType),
                            ),
                        ),
                        th.Property("display_name", th.StringType),
                        th.Property("active", th.BooleanType),
                        th.Property("time_zone", th.StringType),
                        th.Property("account_type", th.StringType),
                        th.Property("email_address", th.StringType),
                    ),
                ),
                th.Property(
                    "status",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("description", th.StringType),
                        th.Property("icon_url", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("id", th.StringType),
                        th.Property(
                            "status_category",
                            th.ObjectType(
                                th.Property("self", th.StringType),
                                th.Property("id", th.IntegerType),
                                th.Property("key", th.StringType),
                                th.Property("color_name", th.StringType),
                                th.Property("name", th.StringType),
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "components",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("self", th.StringType),
                            th.Property("id", th.StringType),
                            th.Property("name", th.StringType),
                        ),
                    ),
                ),
                th.Property("timeoriginalestimate", th.IntegerType),
                th.Property("timetracking", th.StringType),
                th.Property("security", th.StringType),
                th.Property("aggregatetimeestimate", th.IntegerType),
                th.Property("attachment", th.ArrayType(th.StringType)),
                th.Property("summary", th.StringType),
                th.Property(
                    "creator",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("account_id", th.StringType),
                        th.Property("email_address", th.StringType),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType),
                                th.Property("24x24", th.StringType),
                                th.Property("16x16", th.StringType),
                                th.Property("32x32", th.StringType),
                            ),
                        ),
                        th.Property("display_name", th.StringType),
                        th.Property("active", th.BooleanType),
                        th.Property("time_zone", th.StringType),
                        th.Property("account_type", th.StringType),
                    ),
                ),
                th.Property(
                    "subtasks",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("key", th.StringType),
                            th.Property("self", th.StringType),
                            th.Property(
                                "fields",
                                th.ObjectType(
                                    th.Property("summary", th.StringType),
                                    th.Property(
                                        "status",
                                        th.ObjectType(
                                            th.Property("self", th.StringType),
                                            th.Property("description", th.StringType),
                                            th.Property("icon_url", th.StringType),
                                            th.Property("name", th.StringType),
                                            th.Property("id", th.StringType),
                                            th.Property(
                                                "statusCategory",
                                                th.ObjectType(
                                                    th.Property("self", th.StringType),
                                                    th.Property("id", th.IntegerType),
                                                    th.Property("key", th.StringType),
                                                    th.Property("color_name", th.StringType),
                                                    th.Property("name", th.StringType),
                                                ),
                                            ),
                                        ),
                                    ),
                                    th.Property(
                                        "priority",
                                        th.ObjectType(
                                            th.Property("self", th.StringType),
                                            th.Property("icon_url", th.StringType),
                                            th.Property("name", th.StringType),
                                            th.Property("id", th.StringType),
                                        ),
                                    ),
                                    th.Property(
                                        "issuetype",
                                        th.ObjectType(
                                            th.Property("self", th.StringType),
                                            th.Property("id", th.StringType),
                                            th.Property("description", th.StringType),
                                            th.Property("icon_url", th.StringType),
                                            th.Property("name", th.StringType),
                                            th.Property("subtask", th.BooleanType),
                                            th.Property("avatar_id", th.IntegerType),
                                            th.Property("entity_id", th.StringType),
                                            th.Property("hierarchy_level", th.IntegerType),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "reporter",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("account_id", th.StringType),
                        th.Property("email_address", th.StringType),
                        th.Property(
                            "avatar_urls",
                            th.ObjectType(
                                th.Property("48x48", th.StringType),
                                th.Property("24x24", th.StringType),
                                th.Property("16x16", th.StringType),
                                th.Property("32x32", th.StringType),
                            ),
                        ),
                        th.Property("display_name", th.StringType),
                        th.Property("active", th.BooleanType),
                        th.Property("time_zone", th.StringType),
                        th.Property("account_type", th.StringType),
                    ),
                ),
                th.Property(
                    "aggregateprogress",
                    th.ObjectType(
                        th.Property("progress", th.IntegerType),
                        th.Property("total", th.IntegerType),
                        th.Property("percent", th.IntegerType),
                    ),
                ),
                th.Property(
                    "environment",
                    th.ObjectType(
                        th.Property("type", th.StringType),
                        th.Property(
                            "content",
                            th.ArrayType(
                                th.ObjectType(
                                    th.Property(
                                        "content",
                                        th.ArrayType(
                                            th.ObjectType(
                                                th.Property("text", th.StringType),
                                                th.Property("type", th.StringType),
                                            ),
                                        ),
                                    ),
                                    th.Property("type", th.StringType),
                                ),
                            ),
                        ),
                        th.Property("text", th.StringType),
                        th.Property("version", th.IntegerType),
                    ),
                ),
                th.Property("duedate", th.StringType),
                th.Property(
                    "progress",
                    th.ObjectType(
                        th.Property("progress", th.IntegerType),
                        th.Property("total", th.IntegerType),
                    ),
                ),
                th.Property("comment", th.StringType),
                th.Property(
                    "votes",
                    th.ObjectType(
                        th.Property("self", th.StringType),
                        th.Property("votes", th.IntegerType),
                        th.Property("has_voted", th.BooleanType),
                    ),
                ),
                th.Property("worklog", th.StringType),
                th.Property("key", th.StringType),
                th.Property("id", th.IntegerType),
                th.Property("editmeta", th.StringType),
                th.Property("histories", th.StringType),
            ),
        ),
        th.Property("created", th.DateTimeType),
        th.Property("updated", th.DateTimeType),
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

        jql.append(f"updated>='{self.get_starting_timestamp(context).strftime('%Y/%m/%d %H:%M')}'")

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
        new_row = row
        new_row["created"] = row["fields"]["created"]
        new_row["updated"] = row["fields"]["updated"]
        return super().post_process(new_row, context)

    def get_child_context(self, record: dict, context: dict | None) -> dict:  # noqa: ARG002
        """Return a context dictionary for child streams."""
        return {"issue_id": record["id"]}
