import json
import xmltodict

from faker import Faker
from time import perf_counter
from contextlib import contextmanager


class ResponseDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@contextmanager
def check_execution_duration():
    """
    Measures execution duration via context manager end returns callable object with execution time in seconds
    :return: lambda() -> execution time
    """
    __start = perf_counter()
    yield lambda: perf_counter() - __start


def log_http_request(logger, response, request_data=None, get_request=None):
    if get_request is None:
        logger.info(f"Request body: {request_data}")
        logger.info(f"Request {response.request.method}: {response.url}")
        logger.info(f"Response headers: {response.headers}")
        logger.info(f"Response body: {response.text}")
        logger.info(f"Response code: {response.status_code}")
    else:
        logger.info(f"Request {response.request.method}: {response.url}")
        logger.info(f"Response code: {response.status_code}")


def get_result(xml):
    response = json.dumps(xmltodict.parse(xml, xml_attribs=False))
    response = json.loads(response)
    return response['result']


class Fake(Faker):
    Faker(locale=("ru_RU", "en"))
    pass
