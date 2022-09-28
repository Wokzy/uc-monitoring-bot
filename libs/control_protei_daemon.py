import os
import time

from libs.logger import create_logger

logger = create_logger()


class ControlProteiDaemon:

    @staticmethod
    def stop(service: str = None):
        stream = os.popen(f"protei-daemon stop {service}")
        stream.read()
        logger.info(f'Service {service} stopped')

    @staticmethod
    def start(service: str = None):
        stream = os.popen(f"protei-daemon start {service}")
        stream.read()
        logger.info(f'Service {service} started')
        time.sleep(5)

    @staticmethod
    def restart(service: str = None):
        stream = os.popen(f"protei-daemon restart {service}")
        stream.read()
        logger.info(f'Service {service} restarted')
        time.sleep(5)
