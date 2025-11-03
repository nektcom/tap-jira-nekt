"""tap-jira tap class."""

from __future__ import annotations

from nekt_singer_sdk import Tap
from nekt_singer_sdk import typing as th  # JSON schema typing helpers

from tap_jira_nekt.client import JiraStream
from tap_jira_nekt.streams import (
    BoardStream,
    FieldsStream,
    IssueChangeLogStream,
    IssueStream,
    IssueTypeStream,
    ProjectStream,
    SprintStream,
    UsersStream,
)


class TapJira(Tap):
    """tap-jira tap class."""

    name = "tap-jira-nekt"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest record date to sync",
        ),
        th.Property(
            "domain",
            th.StringType,
            description="The Domain for your Jira account, e.g. meltano.atlassian.net",
            required=True,
        ),
        th.Property(
            "api_token",
            th.StringType,
            description="Jira API Token.",
            required=True,
            secret=True,
            title="API Token",
        ),
        th.Property(
            "email",
            th.StringType,
            description="The user email for your Jira account.",
            required=True,
        ),
        th.Property(
            "stream_options",
            th.ObjectType(
                th.Property(
                    "issues",
                    th.ObjectType(
                        th.Property(
                            "jql",
                            th.StringType,
                            description="A JQL query to filter issues",
                            title="JQL Query",
                        ),
                    ),
                    title="Issues Stream Options",
                    description="Options specific to the issues stream",
                ),
            ),
            description="Options for individual streams",
        ),
    ).to_dict()

    def discover_streams(self) -> list[JiraStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            # UsersStream(self),
            # FieldsStream(self),
            # IssueTypeStream(self),
            # ProjectStream(self),
            IssueStream(self),
            # SprintStream(self),
            # BoardStream(self),
            IssueChangeLogStream(self),
        ]
