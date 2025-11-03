"""REST client handling, including tap-jiraStream base class."""

from __future__ import annotations

import typing as t

import inflection
import requests
import requests.auth
from nekt_singer_sdk.helpers.types import Context
from nekt_singer_sdk.record_cleanser import RecordCleanser
from nekt_singer_sdk.streams import RESTStream

from tap_jira_nekt.paginator import PAGE_SIZE, JiraOffsetPaginator

if t.TYPE_CHECKING:
    from nekt_singer_sdk.helpers.types import Context

_Auth = t.Callable[[requests.PreparedRequest], requests.PreparedRequest]


class JiraStream(RESTStream):
    """tap-jira stream class."""

    records_jsonpath = "$[*]"
    record_cleanser = RecordCleanser()

    @property
    def url_base(self) -> str:
        """Returns base url."""
        domain = self.config["domain"]
        return f"https://{domain}:443/rest/api/3"

    @property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return requests.auth.HTTPBasicAuth(
            password=self.config["api_token"],
            username=self.config["email"],
        )

    def get_new_paginator(self) -> JiraOffsetPaginator:
        return JiraOffsetPaginator(start_value=0, page_size=PAGE_SIZE)

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        params["maxResults"] = PAGE_SIZE
        if next_page_token:
            params["startAt"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def convert_keys_to_snake_case(self, obj):
        if isinstance(obj, dict):
            return {inflection.underscore(k): self.convert_keys_to_snake_case(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_keys_to_snake_case(item) for item in obj]
        else:
            return obj

    def validate_response(self, response: requests.Response) -> None:
        return super().validate_response(response)

    def post_process(self, row: dict[str, t.Any], context: t.Mapping[str, t.Any] | None = None) -> dict | None:
        new_row = self.convert_keys_to_snake_case(row)
        return super().post_process(self.record_cleanser.cleanse_record(new_row, self.schema), context)
