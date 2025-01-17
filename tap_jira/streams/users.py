"""Stream type classes for tap-jira."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jira.client import JiraStream

if t.TYPE_CHECKING:
    import requests


class UsersStream(JiraStream):
    name = "users"
    path = "/users/search"
    primary_keys = ["account_id"]
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("self", th.StringType),
        th.Property("key", th.StringType),
        th.Property("account_id", th.StringType),
        th.Property("account_type", th.StringType),
        th.Property("email_address", th.StringType),
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
        th.Property("display_Name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("time_zone", th.StringType),
        th.Property("locale", th.StringType),
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
