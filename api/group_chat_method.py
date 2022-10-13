"""Swagger_API для отправки запросов group chat на сервис uc-access-layer-web"""
import random

from libs.utils import Fake
from libs.net.requests import http_post_request as post, http_get_request as get
from models.uc_api.uc_api_models import GeneralRequest, GroupChat, ChatGroupMemberAddResponse,\
     ChatGroupMemberRemoveResponse, ChatEventResponse, ChatEventControlSearch, ChatEventPinNotify, GeneralResponse, GeneralError

fake = Fake()

__author__ = 'Dmitriy Minor'
__all__ = ['BaseAPI', 'ChatApi', 'AttachmentAPI']


class BaseAPI:
    """
    Cборка запроса
    :param data: Тело запроса
    :param endpoint: конечная точка URL
    :param cookie: Уникальный ID сессии
    :param headers: Кастомные заголовки
    """

    def __init__(self, ip, port, data=None, endpoint=None, cookie=None, headers=None, files=None, filename=None, file_type=None,
                 attachment_id=None, url_attach=None, mediasize=None):

        self.endpoint = endpoint
        self.cookies = cookie
        self.headers = headers
        self.attachment_id = attachment_id
        self.data = data
        self.files = files
        self.filename = filename
        self.file_type = file_type
        self.url_attach = url_attach
        self.mediasize = mediasize
        self.ip = ip
        self.port = port

    def send_request_post(self, timeout=None, url=None):
        if not url:
            url = f"{self.ip}:{self.port}/uc/v2/{self.endpoint}"
        request_model = GeneralRequest(method=self.endpoint, id=random.randrange(11111, 99999), payload=self.data)
        response = post(url=url, data=request_model, cookies=self.cookies, headers=self.headers, files=self.files,
                        filename=self.filename, file_type=self.file_type, timeout=timeout, url_attach=self.url_attach,
                        mediasize=self.mediasize)
        return response

    def send_request_get(self, url=None):
        if not url:
            url = f"{self.ip}:{self.port}/uc/v2/{self.endpoint}"
        response = get(url=url,  cookies=self.cookies, attachment_id=self.attachment_id)
        return response


class ChatApi(BaseAPI):

    def group_chat_event_get(self, data):
        """
        Отправляет запрос chat/event/get в WS
        :param data: тело запроса, которое нужно передать в WS
        """

        self.endpoint = "chat/event/get"
        self.data = data
        self.send_request_post()

    def group_chat_event_draft_save(self):
        """ Cборка запроса chat/event/draft/save """

        self.endpoint = "chat/event/draft/save"
        return self.send_request_post()

    def group_chat_event_draft_delete(self):
        """ Cборка запроса chat/event/draft/delete """

        self.endpoint = "chat/event/draft/delete"
        return self.send_request_post()

    def group_chat_event_send(self, url=None):
        """ Cборка запроса /chat/event/send """

        self.endpoint = "chat/event/send"
        response = self.send_request_post(url=url)
        if response.status_code == 200 or response.status_code == 206:
            response.payload = ChatEventResponse(**response.payload)
        return response

    def group_chat_create(self, url=None):
        """ Cборка запроса /chat/group/create """

        self.endpoint = "chat/group/create"
        response = self.send_request_post()
        if response.status_code == 201:
            response.payload = GroupChat(**response.payload)
        return response

    def group_chat_info(self):
        """ Cборка запроса chat/group/info """

        self.endpoint = "chat/group/info"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = GroupChat(**response.payload)
        return response

    def group_chat_delete(self):
        """ Cборка запроса /chat/group/delete """

        self.endpoint = "chat/group/delete"
        response = self.send_request_post()
        return response

    def group_chat_member_add(self):
        """ Cборка запроса /chat/group/member/add """

        self.endpoint = "chat/group/member/add"
        response = self.send_request_post()
        if response.get("payload"):
            response.payload = ChatGroupMemberAddResponse(**response.payload)
        return response

    def group_chat_member_remove(self):
        """ Cборка запроса /chat/group/member/remove """

        self.endpoint = "chat/group/member/remove"
        response = self.send_request_post()
        if response.get("payload"):
            response.payload = ChatGroupMemberRemoveResponse(**response.payload)
        return response

    def search_msg(self):
        """ Сборка запроса /chat/event/search"""

        self.endpoint = "chat/event/search"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response.payload)
        return response

    def search_msg_continue(self):
        """ Сборка запроса /chat/event/search/continue"""

        self.endpoint = "chat/event/search/continue"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response)
        return response

    def search_msg_stop(self):
        """ Сборка запроса /chat/event/search/stop"""

        self.endpoint = "chat/event/search/stop"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response)
        return response

    def group_chat_msg_pin(self):
        """ Сборка запроса chat/event/pin"""

        self.endpoint = "chat/event/pin"
        response = self.send_request_post()
        if response.status_code == 200:
            response = GeneralResponse(**dict(response.data))
        elif response.status_code == 400:
            response = GeneralError(**dict(response.data))
        return response

    def group_chat_msg_unpin(self):
        """ Сборка запроса chat/event/unpin"""

        self.endpoint = "chat/event/unpin"
        response = self.send_request_post()

        if response.status_code == 200:
            response = GeneralResponse(**dict(response.data))
        elif response.status_code == 400:
            response = GeneralError(**dict(response.data))
        return response

    def mute_chat_group(self):
        """ Сборка запроса chat/notifications/disable"""

        self.endpoint = "chat/notifications/disable"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response)
        return response

    def unmute_chat_group(self):
        """ Сборка запроса chat/notifications/enable"""

        self.endpoint = "chat/notifications/enable"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response)
        return response


class AttachmentAPI(BaseAPI):

    def upload_file(self, files, filename, file_type=None):
        """ Cборка запроса /attachment/upload """

        self.endpoint = "attachment/upload"
        self.files = files
        self.filename = filename
        self.file_type = file_type
        response = self.send_request_post(timeout=5)
        return response

    def download_file(self, attachment_id):
        """ Cборка запроса /attachment/download """

        self.endpoint = "attachment/download"
        self.attachment_id = attachment_id
        response = self.send_request_get()
        return response

    def delete_file(self, attachment_id):
        """ Cборка запроса /attachment/delete"""

        self.endpoint = "attachment/delete"
        self.data = {"ProteiUCAttachmentId": attachment_id}

        response = self.send_request_post()
        return response

    def upload_remote_file(self, url_attach, filename, files, mediasize, file_type=None):
        """ Cборка запроса /attachment/upload/remote """

        self.endpoint = "attachment/upload/remote"
        self.url_attach = url_attach
        self.mediasize = mediasize
        self.filename = filename
        self.files = files
        self.file_type = file_type
        response = self.send_request_post(timeout=10)
        return response

