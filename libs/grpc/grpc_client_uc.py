import grpc
import logging
import configs.config as config

logger = logging.getLogger()


class GRPCClient:
    """
    Client for gRPC functionality
    """

    def __init__(self, host: str = config.IP_UC_ACCESS_LAYER_WEB, port: int = 8314):
        self.host = host
        self.port = port

    def connect(self):
        # instantiate a channel
        return grpc.insecure_channel(f'{self.host}:{self.port}')