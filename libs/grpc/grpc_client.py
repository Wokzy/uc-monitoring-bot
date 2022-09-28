import grpc
import logging
import api.grpc.uc_mcptt_gw_service_pb2 as pb2
import api.grpc.uc_mcptt_gw_service_pb2_grpc as pb2_grpc

logger = logging.getLogger()


class GRPCClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = '127.0.0.1'
        self.server_port = 8314

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.UCMcpttGWStub(self.channel)

    def change_status_register(self, uri, status):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2.UserRegistrationChangedEvent(mcptt_uri=uri, status=status)
        msg = pb2.UserRegistrationChangedRequest(registrations=[message])
        logger.info(f"GRPC CLIENT send msg {msg}")
        return self.stub.OnUserRegistrationChanged(msg)
