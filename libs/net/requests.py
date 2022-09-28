# -*- coding: utf-8 -*-

import urllib3
import logging

from typing import Any
from requests import post, get
from libs.utils import ResponseDict
from libs.utils import log_http_request
from constants import LOG_HTTP_TRAFFIC
from models.uc_api.uc_api_models import GeneralResponse, GeneralError

logger = logging.getLogger()


def __make_cookies_header(cookies):
    return ';'.join([x + '=' + cookies[x] for x in cookies])


def http_post_request(url: str, data: Any = None, files=None, filename=None, file_type=None, params: dict = None,
                      headers: dict = None, cookies: dict = None, mediasize=None, attachment_id: str = None,
                      timeout: int = 3, url_attach: str = None):
    """
    Send http POST request
    :param url_attach: Ссылка на аттачь
    :param attachment_id: ID вложения
    :param file_type: Тип файла
    :param filename: Имя файла для загрузки
    :param files: Файл для загрузки
    :param timeout: тайм-аут ожидания ответа
    :param url: Server url without http prefix
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    :param params: (optional) Params to urlencode
    :param headers: (optional) Set request headers
    :param cookies: (optional) Set request cookies. Default will be used if not given
    :param mediasize: Размер прикрепляемого thumbnail к вложению
    :return:
    """

    if headers is None:
        headers = {
            "Content-Type": "application/json"
        }

    upload_file = {}

    if cookies is not None:
        headers = {'Content-type': 'application/json', 'protei-uc-sessionid': cookies}
    if filename is not None:
        headers = {'Content-type': file_type, 'protei-uc-sessionid': cookies, 'protei-uc-filename': filename}
        upload_file = open(files, 'rb')
        data_file = upload_file.read()
        data = None
    if mediasize is not None:
        headers = {'Content-type': file_type, 'protei-uc-sessionid': cookies, 'protei-uc-filename': filename,
                   'protei-uc-mediasize': mediasize, 'protei-uc-attachmentid': attachment_id}
        upload_file = open(files, 'rb')
        data_file = upload_file.read()
        data = None
    if url_attach is not None:
        headers = {'Content-type': file_type, 'Protei-Uc-Sessionid': cookies, 'protei-uc-filename': filename,
                   'protei-uc-mediaremoteurl': url_attach, "protei-uc-mediasize": mediasize}
        upload_file = open(files, 'rb')
        data_file = upload_file.read()
        data = None

    __request_url = f"http://{url}"

    try:
        if data is not None:
            response = post(url=__request_url, data=data.json(by_alias=True, exclude_none=True), params=params, headers=headers, timeout=timeout, files=upload_file)
            if 400 <= response.status_code <= 500:
                response_id = GeneralError(**response.json()).id
                response_dict = ResponseDict({"headers": response.headers, "data": GeneralError(**response.json()),
                                              "payload": response.json().get("payload", None),
                                              "status_code": response.status_code})
            else:
                response_id = GeneralResponse(**response.json()).id
                response_dict = ResponseDict({"headers": response.headers, "data": GeneralResponse(**response.json()),
                                              "payload": response.json().get("payload", None),
                                              "status_code": response.status_code})
            request_id = data.id
            assert request_id == response_id
        else:
            response = post(url=__request_url, data=data_file, params=params, headers=headers, timeout=timeout)
            if 400 <= response.status_code <= 500:
                response_dict = ResponseDict({"headers": response.headers, "data": GeneralError(**response.json()),
                                              "payload": response.json().get("payload", None),
                                              "status_code": response.status_code})
            else:
                response_dict = ResponseDict({"headers": response.headers, "status_code": response.status_code})
                return response_dict, int(response.request.headers["Content-Length"])

    except urllib3.exceptions.ConnectTimeoutError as e:
        logger.error(f"Error: {e}")
        raise
    except Exception as error:
        logger.error(f"Error: {error}")
        raise

    if LOG_HTTP_TRAFFIC:
        log_http_request(logger, response, data)

    return response_dict


def http_get_request(url: str, headers: dict = None, cookies: dict = None, attachment_id: str = None, data=None,
                     mediasize=None, timeout: int = 3, stream = None):
    """
    Send http GET request
    :param url: Server url without http prefix
    :param headers: (optional) Set request headers
    :param attachment_id: Set protei-uc-attachmentid
    :param cookies: (optional) Set request cookies. Default will be used if not given
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    :return:
    """

    if headers is None:
        headers = {'protei-uc-sessionid': cookies, 'protei-uc-attachmentid': attachment_id}
    if mediasize is not None:
        headers = {'protei-uc-sessionid': cookies, 'protei-uc-mediasize': mediasize,
                   'protei-uc-attachmentid': attachment_id}

    __request_url = f"http://{url}"

    try:
        if headers.get("protei-uc-attachmentid"):
            with get(url=__request_url, headers=headers, stream=True) as response:
                if 400 <= response.status_code <= 500:
                    response_dict = ResponseDict({"headers": response.headers, "data": GeneralError(**response.json()),
                                                  "payload": response.json().get("payload", None),
                                                  "status_code": response.status_code})
                    return response_dict
                with open('file', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            try:
                if response.raise_for_status() is not None:
                    response_dict = ResponseDict({"headers": response.headers, "data": GeneralError(**response.json()),
                                                  "payload": response.json().get("payload", None),
                                                  "status_code": response.status_code})
                    return response_dict
                else:
                    response_dict = ResponseDict({"headers": response.headers,
                                                  "status_code": response.status_code})
                    return response_dict
            except Exception:
                pass
        else:
            headers = {"Upgrade": "websocket", "Connection": "Upgrade", "Sec-WebSocket-Key": "eS6wH8nUyl8u1UMACnizuw==",
                       "Sec-WebSocket-Version": "13", "Content-Type": "application/json",
                       "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"}
            response = get(url=__request_url, headers=headers, data=data, timeout=timeout, stream=stream)

            if 400 <= response.status_code <= 500:
                response_dict = ResponseDict({"headers": response.headers, "data": GeneralError(**response.json()),
                                              "payload": response.json().get("payload", None),
                                              "status_code": response.status_code})
                return response_dict
            elif response.status_code == 101:
                response_dict = ResponseDict({"headers": response.headers, "status_code": response.status_code})
                return response_dict
            elif stream == True:
                response_dict = ResponseDict({"headers": response.headers, "status_code": response.status_code})
                with open('file', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                return response_dict
            else:
                response_dict = ResponseDict({"headers": response.headers, "data": GeneralResponse(**response.json()),
                                              "payload": response.json().get("payload", None),
                                              "status_code": response.status_code})
                return response_dict

    except urllib3.exceptions.ConnectTimeoutError as e:
        logger.error(f"Error: {e}")
        raise
    except Exception as error:
        logger.error(f"Error: {error}")
        raise

    if LOG_HTTP_TRAFFIC:
        log_http_request(logger, response, get_request=True)
