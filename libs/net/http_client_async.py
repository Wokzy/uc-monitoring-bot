"""!!!!!!!!!!!!!!!!!!!!!1 Модуль НЕ используется !!!!!!!!!!!!!!!!!!!!!!!!!!"""
import queue
import asyncio
import aiohttp
import logging
import threading

from configs.config import IP_UC_ACCESS_LAYER_WEB, PORT_UC_ACCESS_LAYER_WEB

logger = logging.getLogger()

__author__ = 'Dmitriy Minor'
__all__ = ['http_con', 'HttpClient']


def http_con(name: str, ip: str = IP_UC_ACCESS_LAYER_WEB, port: int = PORT_UC_ACCESS_LAYER_WEB):
    """
    :param ip: IP адресс сервиса uc-access-layer-web
    :param port: Порт сервиса uc-access-layer-web
    :param name: имя пользователя, который производит подключение к WS
    """
    request_queue = queue.Queue()
    response_queue = queue.Queue()
    client = HttpClient(request_queue=request_queue, response_queue=response_queue, name=name)
    client.setDaemon(True)
    client.start()
    return client


class HttpClient(threading.Thread):
    """
    :param request: URL по которому осуществляется соединение с WS
    :param request_queue: очередь с тасками, в которой хранятся сообщения для отправки
    :param response_queue: очередь в которую складываются ответы на запросы
    :param name: имя пользователя, который производит подключение к WS
    """

    def __init__(self, request_queue, response_queue, name):
        threading.Thread.__init__(self)
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.name = name

    def run(self):
        asyncio.run(self.main(), debug=True)

    async def main(self):
        async with aiohttp.ClientSession() as client:
            while True:
                try:
                    request = self.request_queue.get_nowait()
                    if request == "Close WS":
                        logger.info(f"{self.name} closed HTTP connection")
                        await client.close()
                        break
                    async with client.post(url=request["url"], headers=request["headers"],
                                           data=request["data"]) as response:
                        body = await response.json()
                        response_dict = ResponseDict({"headers": response.headers, "data": body,
                                                      "payload": body.get("payload", None),
                                                      "status_code": response.status, "name": self.name})
                        self.response_queue.put(response_dict)
                except queue.Empty:
                    await asyncio.sleep(0.1)


class ResponseDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__