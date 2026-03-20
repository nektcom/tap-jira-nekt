"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream
from tap_jira_nekt.streams.projects import ProjectStream


class FieldsStream(JiraStream):
    name = "fields"
    path = "/field/search"
    records_jsonpath = "$.values[*]"
    primary_keys = ["id"]
    instance_name = "values"
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
        th.Property("id", th.StringType, description="Unique identifier of the record."),
        th.Property("key", th.StringType, description="Unique key of the record."),
        th.Property("name", th.StringType, description="Name of the record."),
        th.Property("untranslated_name", th.StringType, description="Untranslated name of the record."),
        th.Property("custom", th.BooleanType, description="Indicates whether the field is custom."),
        th.Property("orderable", th.BooleanType, description="Indicates whether the field can be used for ordering."),
        th.Property("navigable", th.BooleanType, description="Indicates whether the field is visible in navigation."),
        th.Property("searchable", th.BooleanType, description="Indicates whether the field can be used in search."),
        th.Property("clause_names", th.ArrayType(th.StringType), description="Clause names of the record."),
        th.Property(
            "scope",
            th.ObjectType(
                th.Property("type", th.StringType, description="Type classification of the record."),
                th.Property(
                    "project",
                    th.ObjectType(
                        th.Property("id", th.StringType, description="Unique identifier of the record."),
                    ),
                
                    description="Project of the record."),
            ),
        
            description="Scope of the record."),
        th.Property(
            "schema",
            th.ObjectType(
                th.Property("type", th.StringType, description="Type classification of the record."),
                th.Property("system", th.StringType, description="System of the record."),
                th.Property("items", th.StringType, description="Items of the record."),
                th.Property("custom", th.StringType, description="Indicates whether the field is custom."),
                th.Property("custom_id", th.IntegerType, description="Identifier of the associated custom."),
                th.Property(
                    "configuration",
                    th.ObjectType(
                        th.Property("custom_renderer", th.BooleanType, description="Custom renderer of the record."),
                        th.Property("read_only", th.BooleanType, description="Read only of the record."),
                        th.Property("environment", th.StringType, description="Environment of the record."),
                    ),
                
                    description="Configuration of the record."),
            ),
        
            description="Schema of the record."),
    ).to_dict()
