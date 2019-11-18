"""
This file contains helper functions used by the tests
"""
import json
import os

from collections import deque


class DummyContent:
    """
    Proxy response to simulate request object return for an url
    """
    def __init__(self, url, params=None):
        self.status_code = 200
        self.url = url

    def raise_for_status(self):
        if not self.status_code == 200:
            raise Exception()

    def json_response(self) -> str:
        # assuming tests are run from directory of this module
        current_dir = os.getcwd()
        with open('{}/response.json'.format(current_dir)) as file:
            response = file.read()
            file.close()
            return response


def get_key_values(json_dict: dict, key: str, root="root") -> dict:
    """
    General function using BFS to traverse provided json dict
    to extract values for specified key.

    :param json_dict: dict, json response
    :param key: str, specified key to look for
    :param root: str, specified base path/location for the json_dct provided
    :return: dict[location]=content, where:
            - content is the value stored in the json for the specified key
            - location (str) is the path of keys upto + including the specified key.
                    Information for better error messages
    """
    PREVPATH_AND_KEY = '{}[{}]'
    return_content = {}
    if not json_dict or not key:
        return return_content
    # double sided queue to store areas of json to traverse for key
    q = deque([
        (json_dict, root)
    ])

    # bfs traversal
    while q:
        json_section, path = q.popleft()

        # if a dict look for the specified key
        if isinstance(json_section, dict):
            # if key not found, append all dict.values() to queue for traversing
            if json_section.get(key, "Not found") == "Not found":
                for k, value in json_section.items():
                    q.append(
                        (value, PREVPATH_AND_KEY.format(path, k))
                    )
            # else, add the found key to the return
            else:
                return_content[PREVPATH_AND_KEY.format(path, key)] = json_section[key]
        # if list, append all of the list to the queue
        elif isinstance(json_section, list):
            for index, value in enumerate(json_section):
                q.append(
                    (value, PREVPATH_AND_KEY.format(path, index))
                )

        # not covered:
        # scenario where key is found in dict and we want to both
        # record found key's values and traverse other keys in the same dict

    return return_content


def verify_status_ok(url: str, params: dict) -> DummyContent:
    """
    Gets info from the url and checks the response from the request.
    If status is not OK, raises an exception with a custom message

    :param url: str, the url, such as "https://validate.test.com"
    :param params: dict, payload converted from a json string
    :return: response object
    """
    response = DummyContent(url, params)
    if not response.status_code == 200:
        raise Exception("Got status {} from {}"
                        .format(response.status_code, response.url))
    return response


def request_get_content(url: str, payload: dict) -> dict:
    """
    Checks status of the response and returns the content received.

    :param url: str, url to send payload to
    :param payload: str, json in string format
    :return: dict, response
    """
    # will raise an exception if status is not ok
    response = verify_status_ok(url, params=payload)

    return json.loads(response.json_response())
