"""Swagger_API для создания подключения к WS uc-access-layer-web"""
import time
import json
import queue
import asyncio
import logging
import threading
import websockets

from api.http_api.uc.system_method import SystemApi
from models.uc_api.uc_api_models import GeneralEvent
from configs.config import IP_UC_ACCESS_LAYER_WEB, PORT_UC_ACCESS_LAYER_WEB

logger = logging.getLogger()

__author__ = 'Dmitriy Minor'
__all__ = ['ws_con', 'WSConnection']


def request_queue_list(args):
    pass


def ws_con(protei_uc_sessionid: str, name: str, ip: str = IP_UC_ACCESS_LAYER_WEB, port: int = PORT_UC_ACCESS_LAYER_WEB):
    """
    :param ip: IP адресс сервиса uc-access-layer-web
    :param port: Порт сервиса uc-access-layer-web
    :param protei_uc_sessionid: Уникальный Id сессии
    :param name: имя пользователя, который производит подключение к WS
    """
    request_queue = queue.Queue()
    response_queue = queue.Queue()
    response_queue_list = queue.Queue()
    ws_id = SystemApi(cookie=protei_uc_sessionid).websocket_token_generate()
    url_ws = f"ws://{ip}:{port}/uc/v2/websocket/{ws_id.payload.token}"
    ws = WSConnection(ws_url=url_ws, request_queue=request_queue, response_queue_list=response_queue_list,
                      response_queue=response_queue, name=name)
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

    def __init__(self, ws_url, request_queue, response_queue, response_queue_list, name):
        threading.Thread.__init__(self)
        self.ws_url = ws_url
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.response_queue_list = response_queue_list
        self.name = name

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
        recv_msg_list = list()
        while True:
            recv_msg = await ws.recv()
            recv_msg_list.append(recv_msg[8:])
            logger.info(f"Response message in WS {self.name}: {recv_msg[8:]}")
            self.response_queue.put(json.loads(recv_msg[8:]))
            self.response_queue_list.put(recv_msg_list)

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
