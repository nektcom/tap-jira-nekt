"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira_nekt.client import JiraStream

if t.TYPE_CHECKING:
    import requests


class UsersStream(JiraStream):
    name = "users"
    path = "/users/search"
    primary_keys = ["account_id"]
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("self", th.StringType, description="URL of the resource."),
        th.Property("key", th.StringType, description="Unique key of the record."),
        th.Property("account_id", th.StringType, description="Identifier of the associated account."),
        th.Property("account_type", th.StringType, description="Account type of the record."),
        th.Property("email_address", th.StringType, description="Email address of the record."),
        th.Property("name", th.StringType, description="Name of the record."),
        th.Property(
            "avatar_urls",
            th.ObjectType(
                th.Property("48x48", th.StringType, description="48x48 of the record."),
                th.Property("24x24", th.StringType, description="24x24 of the record."),
                th.Property("16x16", th.StringType, description="16x16 of the record."),
                th.Property("32x32", th.StringType, description="32x32 of the record."),
            ),
        
            description="URLs related to the avatar."),
        th.Property("display_name", th.StringType, description="Display name of the record."),
        th.Property("active", th.BooleanType, description="Indicates whether the record is active."),
        th.Property("time_zone", th.StringType, description="Time zone of the record."),
        th.Property("locale", th.StringType, description="Locale of the record."),
    ).to_dict()

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: t.Any | None,  # noqa: ANN401
    ) -> t.Any | None:  # noqa: ANN401
        """Return a token for identifying next page or None if no more pages."""
        # If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        resp_json = response.json()
        if previous_token is None:
            previous_token = 0

        page = resp_json
        if len(page) == 0:
            return None

        return previous_token + len(page)
