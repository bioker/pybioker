import logging
from json import loads
from logging import Logger
from typing import Any
from typing import Union

import requests
from requests import Response


def _warn_if_unsuccessful(logger: Logger, response: Response):
    if not response.ok:
        warning_msg = """request to url: %s finished with non-ok response: %s %s %s"""
        logger.warning(warning_msg, response.url, response.status_code, response.headers, response.text)


def _get_response_content(response: Response) -> Any:
    content_type: str = str(response.headers.get('Content-Type'))
    if content_type.startswith('application/json'):
        return loads(response.text)
    elif content_type.startswith('text'):
        return response.text
    return response.content


class HttpClient:

    def __init__(self, base_url: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        self.base_url = base_url

    def request(self, method: str = 'GET', path: str = '', headers: dict = None, params: dict = None,
                data: bytes = None, json: Union[dict, list] = None) -> Any:
        url = self.base_url + path

        response = self.session.request(method, url, headers=headers, params=params, data=data, json=json)
        _warn_if_unsuccessful(self.logger, response)

        return _get_response_content(response)
