"""Swagger_API для отправки запросов chat на сервис uc-access-layer-web"""
import random

from libs.utils import Fake
from libs.net.requests import http_post_request as post, http_get_request as get
from models.uc_api.uc_api_models import P2pChat, ChatEventResponse, GeneralRequest, ChatEventControlSearch, ChatEventPinNotify, \
    GeneralResponse, GeneralError

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
                 attachment_id=None, mediasize=None, stream=None, url_attach=None):

        self.endpoint = endpoint
        self.cookies = cookie
        self.headers = headers
        self.attachment_id = attachment_id
        self.data = data
        self.files = files
        self.filename = filename
        self.file_type = file_type
        self.mediasize = mediasize
        self.stream = stream
        self.url_attach = url_attach
        self.ip = ip
        self.port = port

    def send_request_post(self, timeout=None):
        url = f"{self.ip}:{self.port}/uc/v2/{self.endpoint}"
        request_model = GeneralRequest(method=self.endpoint, id=random.randrange(11111, 99999), payload=self.data)
        response = post(url=url, data=request_model, cookies=self.cookies, headers=self.headers, files=self.files,
                        filename=self.filename, file_type=self.file_type, mediasize=self.mediasize,
                        attachment_id=self.attachment_id, timeout=timeout, url_attach=self.url_attach)
        return response

    def send_request_get(self):
        url = f"{self.ip}:{self.port}/uc/v2/{self.endpoint}"
        response = get(url=url,  cookies=self.cookies, attachment_id=self.attachment_id, mediasize=self.mediasize, stream=self.stream)
        return response


class ChatApi(BaseAPI):

    def p2p_chat_create(self):
        """ Cборка запроса /chat/p2p/create """

        self.endpoint = "chat/p2p/create"
        response = self.send_request_post()
        if response.status_code == 201:
            response.payload = P2pChat(**response.payload)
        return response

    def p2p_chat_event_send(self):
        """ Cборка запроса /chat/event/send """

        self.endpoint = "chat/event/send"
        response = self.send_request_post()
        if response.status_code == 200 or response.status_code == 206:
            response.payload = ChatEventResponse(**response.payload)
        return response

    def p2p_chat_event_change(self):
        """ Cборка запроса chat/change """

        self.endpoint = "chat/event/change"
        response = self.send_request_post()
        if response.status_code == 200 or response.status_code == 206:
            response.payload = ChatEventResponse(**response.payload)
        return response

    def p2p_chat_event_draft_save(self):
        """ Cборка запроса chat/event/draft/save """

        self.endpoint = "chat/event/draft/save"
        return self.send_request_post()

    def p2p_chat_event_draft_delete(self):
        """ Cборка запроса chat/event/draft/delete """

        self.endpoint = "chat/event/draft/delete"
        return self.send_request_post()

    def p2p_chat_info(self):
        """ Cборка запроса chat/p2p/info """

        self.endpoint = "chat/p2p/info"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = P2pChat(**response.payload)
        return response

    def p2p_chat_delete(self):
        """ Cборка запроса /chat/p2p/delete """

        self.endpoint = "chat/p2p/delete"
        response = self.send_request_post()
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

    def p2p_chat_msg_pin(self):
        """ Сборка запроса chat/event/pin"""

        self.endpoint = "chat/event/pin"
        response = self.send_request_post()
        if response.status_code == 200:
            response = GeneralResponse(**dict(response.data))
        elif response.status_code == 400:
            response = GeneralError(**dict(response.data))
        return response

    def p2p_chat_msg_unpin(self):
        """ Сборка запроса chat/event/unpin"""

        self.endpoint = "chat/event/unpin"
        response = self.send_request_post()

        if response.status_code == 200:
            response = GeneralResponse(**dict(response.data))
        elif response.status_code == 400:
            response = GeneralError(**dict(response.data))
        return response

    def mute_chat_p2p(self):
        """ Сборка запроса chat/notifications/disable"""

        self.endpoint = "chat/notifications/disable"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response)
        return response

    def unmute_chat_p2p(self):
        """ Сборка запроса chat/notifications/enable"""

        self.endpoint = "chat/notifications/enable"
        response = self.send_request_post()
        if response.status_code == 200:
            response.payload = ChatEventControlSearch(**response)
        return response


class AttachmentAPI(BaseAPI):

    def __init__(self, ip, port, data=None, endpoint=None, cookie=None, headers=None, files=None, filename=None, file_type=None,
                 attachment_id=None, mediasize=None, stream=None):
        super().__init__(ip, port, data, endpoint, cookie, headers, files, filename, file_type, attachment_id, mediasize, stream)
        self.url_attach = None

    def upload_file(self, files, filename, file_type=None, mediasize=None, 
                    attachment_id=None):
        """ Cборка запроса /attachment/upload """

        self.endpoint = "attachment/upload"
        self.files = files
        self.filename = filename
        self.file_type = file_type
        self.mediasize = mediasize
        self.attachment_id = attachment_id
        response = self.send_request_post(timeout=5)
        return response

    def download_file(self, attachment_id, mediasize=None):
        """ Cборка запроса /attachment/download """

        self.endpoint = "attachment/download"
        self.attachment_id = attachment_id
        self.mediasize = mediasize
        response = self.send_request_get()
        return response

    def download_apk(self, attachment_id=None, mediasize=None, stream=True):
        """ Cборка запроса android/apk/download """

        self.endpoint = "android/apk/download"
        self.attachment_id = attachment_id
        self.mediasize = mediasize
        self.stream = stream
        response = self.send_request_get()

        return response

    def version_apk(self, attachment_id=None, mediasize=None):
        """ Cборка запроса android/apk/version """

        self.endpoint = "android/apk/version"
        self.attachment_id = attachment_id
        self.mediasize = mediasize
        response = self.send_request_get()

        return response

    def delete_file(self, attachment_id, mediasize=None):
        """ Cборка запроса /attachment/delete"""

        self.endpoint = "attachment/delete"
        self.data = {"ProteiUCAttachmentId": attachment_id}
        if mediasize is not None:
            self.data = {"ProteiUCAttachmentId": attachment_id, "ProteiUCMediaSize": mediasize}

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
