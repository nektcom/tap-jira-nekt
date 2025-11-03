import requests
from nekt_singer_sdk.pagination import BaseOffsetPaginator

PAGE_SIZE = 50


class JiraOffsetPaginator(BaseOffsetPaginator):

    def has_more(self, response: requests.Response) -> bool:
        if isinstance(response.json(), list):
            return len(response.json()) == PAGE_SIZE

        return not response.json().get("isLast")
