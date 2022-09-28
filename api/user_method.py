"""Swagger_API для отправки запросов users на сервис uc-access-layer-web"""
import random

from requests import get
from libs.utils import Fake
from libs.net.requests import http_post_request as post
from models.uc_api.uc_api_models import UserInfo, CreateUser, GeneralRequest
from models.uc_api.mcptt_model.mcptt_login_response import MCPTTUserLoginResponse

__author__ = 'Dmitriy Minor'
__all__ = ['BaseAPI', 'UserApi']

fake = Fake()


class BaseAPI:
    """
    Cборка запроса
    :param data: Тело запроса
    :param endpoint: конечная точка URL
    :param cookie: Уникальный ID сессии
    :param headers: Кастомные заголовки
    """

    def __init__(self, ip, port, data=None, endpoint=None, cookie=None,
                 headers=None):
        self.endpoint = endpoint
        self.cookies = cookie
        self.headers = headers
        self.data = data
        self.ip = ip
        self.port = port

    def send_request(self):
        url = f"{self.ip}:{self.port}/uc/v2/{self.endpoint}"
        request_model = GeneralRequest(method=self.endpoint, id=random.randrange(11111, 99999), payload=self.data)
        response = post(url=url, data=request_model, cookies=self.cookies, headers=self.headers)
        return response

    def send_request_get(self):
        url = f"http://{self.ip}:{self.port}/uc/v2/{self.endpoint}"
        response = get(url=url, headers=self.headers, stream=True)
        return response


class UserApi(BaseAPI):

    def login(self):
        """ Cборка запроса login """

        self.endpoint = "login"
        response = self.send_request()
        if response.status_code == 206:
            response.payload = UserInfo(**response.payload)
        elif 400 <= response.status_code <= 500:
            return response
        elif response.status_code == 209:
            if response.get("payload"):
                response.payload = UserInfo(**response.payload)
        else:
            response.payload = UserInfo(**response.payload)
        return response

    def mcptt_group_get(self, group_name):
        """ Cборка запроса login """

        self.endpoint = f"mcptt/gw/org.openmobilealliance.groups/global/byGroupID/{group_name}"
        response = self.send_request_get()
        return response

    def mcptt_login(self):
        """ Cборка запроса mcptt/login """

        self.endpoint = "mcptt/login"
        response = self.send_request()
        if response.status_code == 206:
            response.payload = MCPTTUserLoginResponse(**response.payload)
        elif 400 <= response.status_code <= 500:
            return response
        elif response.status_code == 209:
            if response.get("payload"):
                response.payload = MCPTTUserLoginResponse(**response.payload)
        else:
            response.payload = MCPTTUserLoginResponse(**response.payload)
        return response

    def user_info(self):
        """ Сборка запроса с user/info """

        self.endpoint = "user/info"
        response = self.send_request()
        if response.status_code == 201:
            response.payload = CreateUser(**response.payload)
        elif response.status_code == 200 or response.status_code == 206:
            payload = []
            for i in response.payload:
                payload.append(UserInfo(**i))
            response.payload = payload
        return response

    def logout(self):
        """ Cборка запроса logout """

        self.endpoint = "logout"
        response = self.send_request()
        return response

    def user_set(self):
        """ Сборка запроса с user/set """

        self.endpoint = "user/set"
        response = self.send_request()
        if response.status_code == 201:
            response.payload = CreateUser(**response.payload)
        elif response.status_code == 409:
            payload = []
            for i in response.data.entity:
                payload.append(UserInfo(**i))
            response.payload = payload
        return response

    def user_snapshot(self):
        """ Сборка запросов с user/snapshot """

        self.endpoint = "user/snapshot"
        response = self.send_request()
        if response.status_code == 201:
            response.payload = CreateUser(**response.payload)
        return response

    def user_set_last_activity(self):
        """Сборка запросов user/set/last_activity"""

        self.endpoint = "user/set/last_activity"
        response = self.send_request()
        return response

    def user_delete(self, data):
        """Сборка запросов user/delete"""

        self.endpoint = "user/delete"
        self.data = data
        response = self.send_request()
        return response
