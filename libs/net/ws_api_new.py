"""Swagger_API для создания подключения к WS uc-access-layer-web"""
import time
import json
import queue
import asyncio
import logging
import threading
import websockets

from pydantic.error_wrappers import ValidationError
from api.http_api.uc.system_method import SystemApi
from models.uc_api.uc_api_models import GeneralEvent
from configs.config import IP_UC_ACCESS_LAYER_WEB, PORT_UC_ACCESS_LAYER_WEB

logger = logging.getLogger()

__author__ = 'Dmitriy Minor'
__all__ = ['ws_con', 'WSConnection']


def ws_con(protei_uc_sessionid: str, name: str, ip: str = IP_UC_ACCESS_LAYER_WEB,
           port: int = PORT_UC_ACCESS_LAYER_WEB):
    """
    :param ip: IP адресс сервиса uc-access-layer-web
    :param port: Порт сервиса uc-access-layer-web
    :param protei_uc_sessionid: Уникальный Id сессии
    :param name: имя пользователя, который производит подключение к WS
    """
    task_queue = queue.Queue()
    request_queue = queue.Queue()
    ws_id = SystemApi(cookie=protei_uc_sessionid, ip=ip, port=port).websocket_token_generate()
    url_ws = f"ws://{ip}:{port}/uc/v2/websocket/{ws_id.payload.token}"
    ws = WSConnection(ws_url=url_ws, request_queue=request_queue, task_queue=task_queue, name=name)
    ws.setDaemon(True)
    ws.start()
    time.sleep(0.3)
    return ws


class WSConnection(threading.Thread):
    """
    :param ws_url: URL по которому осуществляется соединение с WS
    :param request_queue: очередь с тасками, в которой хранятся сообщения для отправки
    :param response_queue: очередь в которую складываются ответы на запросы
    :param name: имя пользователя, который производит подключение к WS
    """

    def __init__(self, ws_url, request_queue, task_queue, name):
        threading.Thread.__init__(self)
        self.ws_url = ws_url
        self.task_queue = task_queue
        self.request_queue = request_queue
        self.name = name
        self.response = {}

    def wait_ws(self, tasks: list):
        for task in tasks:
            self.task_queue.put(task)

    def get_ws(self, msg, result: bool = True, count=3):
        if result:
            for i in range(0, count):
                try:
                    return self.response[msg].pop()
                except IndexError:
                    time.sleep(1)
                except KeyError:
                    time.sleep(1)
            logger.error(f"{msg} is empty")
            assert result is False
        else:
            general_error = None
            for i in range(0, count):
                try:
                    general_error = self.response[msg].pop()
                except IndexError:
                    time.sleep(1)
                except KeyError:
                    time.sleep(1)
            assert general_error is None
            logger.info(f"{msg} is empty. This is a successful result")

    def run(self):
        asyncio.run(self.main(), debug=True)

    async def main(self):
        async with websockets.connect(self.ws_url, close_timeout=0.5, max_size=100000000) as websocket:
            logger.info(f"{self.name} connect to Websocket")
            first_response = await websocket.recv()
            GeneralEvent(**json.loads(first_response[8:]))
            await asyncio.gather(self.recvMsg(websocket),
                                 self.sendMsg(websocket), return_exceptions=asyncio.FIRST_COMPLETED)

    async def recvMsg(self, ws):
        while True:
            recv_msg = await ws.recv()
            recv_msg = recv_msg[8:]
            logger.info(f"Response message in WS {self.name}: {recv_msg}")
            if not self.task_queue.empty():
                for i in range(self.task_queue.qsize()):
                    task = self.task_queue.get()
                    try:
                        dict_msg = json.loads(recv_msg)
                        response = task(**dict_msg)
                        task_name = task.__name__
                        logger.info(f"Successful validated message in WS {self.name}")
                        if self.response.get(task_name, False):
                            self.response[task_name].append(response)
                        else:
                            self.response[task_name] = [response]
                        break
                    except ValidationError:
                        self.task_queue.put(task)
                        logger.info(f"Failed validated message in WS {self.name}")
            else:
                logger.info("All WS task validated")

    async def sendMsg(self, ws):
        check_ws_con = 0
        while True:
            try:
                send_msg = self.request_queue.get_nowait()
                if send_msg == "Close WS":
                    logger.info(f"{self.name} closed connect Websocket")
                    await ws.close()
                    break
                send_msg = send_msg.json(by_alias=True, exclude_none=True)
                logger.info(f"Request message in WS {self.name}: {send_msg}")
                self.request_queue.task_done()
                await ws.send(send_msg)
            except queue.Empty:
                await asyncio.sleep(0.1)
                if check_ws_con != 1800:
                    check_ws_con += 1
                else:
                    logger.info(f"{self.name} closed connect Websocket")
                    await ws.close()
                    break
