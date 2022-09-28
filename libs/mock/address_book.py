
import sys
import queue
import logging
import asyncio
import multiprocessing

from aiohttp import web
from queue import Queue
from configs.config import IP_ADDRESS_BOOK_MOCK, PORT_ADDRESS_BOOK_MOCK

__author__ = 'Dmitriy Minor'
__all__ = ['address_book_con']

logger = logging.getLogger()


def address_book_con(ip: str = IP_ADDRESS_BOOK_MOCK, port: int = PORT_ADDRESS_BOOK_MOCK):
    """
    :param ip: IP адресс сервиса uc-access-layer-web
    :param port: Порт сервиса uc-access-layer-web
    """

    request_queue = Queue()
    response_queue = multiprocessing.Queue()
    ab_srv = AddressBookSrv(request_queue=request_queue, response_queue=response_queue, ip=ip, port=port)
    ab_srv.start()
    return ab_srv


class AddressBookSrv(multiprocessing.Process):

    def __init__(self, request_queue, response_queue, ip, port):
        multiprocessing.Process.__init__(self)
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.ip = ip
        self.port = port

    def run(self):
        self.run_server(self.handler())

    def handler(self):

        async def login(request):
            body_dict = {}
            async for body in request.content:
                for line in body.decode().split('&'):
                    key, value = [word.strip() for word in line.split("=")]
                    body_dict[key] = value
                if body_dict.get("username") == "admin" and body_dict.get("password") == "password":
                    return web.Response(text='{"id":1,"username":"admin","role":"ROLE_SYSADMIN","categories":[]}',
                                        headers={"Set-Cookie": "JSESSIONID_8280=n0w1m628km2ug12vh0xan3q;Path=/",
                                                 "Expires": "Thu, 01 Jan 1970 00:00: 00GMT"})
                else:
                    sys.exit(1)

        async def search_contact(request):

            while True:
                try:
                    request_list = []
                    response = self.response_queue.get_nowait()
                    async for body in request.content:
                        request_list.append(body.decode())
                    logger.info(f"Request to Address Book: {request_list}")
                    logger.info(f"Response from Address Book {response['data']}")
                    return web.Response(text=response["data"], headers=response["headers"], status=response["status_code"], content_type="text/xml")
                except queue.Empty:
                    await asyncio.sleep(0.1)

        app = web.Application()
        app.router.add_post('/ContactService', search_contact)
        app.router.add_post('/login', login)
        runner = web.AppRunner(app)

        return runner

    def run_server(self, runner):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host=self.ip, port=self.port)
        loop.run_until_complete(site.start())
        loop.run_forever()
