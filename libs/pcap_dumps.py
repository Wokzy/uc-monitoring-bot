import os
import sys
import time
import pyshark
import threading

from configs.config import *


PORTS = [PORT_UC_ACCESS_LAYER_WEB, PORT_UC_MESSAGE_SNAPSHOT_GRPC, PORT_UC_IN_GRPC, PORT_UC_POST_GRPC,
         PORT_UC_ROUTE_GRPC,
         PORT_UC_USER_STORAGE, PORT_UC_USER_MESSAGE_STORE_SRV, AUTH_GATEWAY_SRV_ENDPOINT, PLUGIN_SRV_ENDPOINT,
         VCS_ADAPTER_ENDPOINT,
         ADDRESS_BOOK_SRV_ENDPOINT, GROUP_SRV_ENDPOINT, PUSH_SRV_ENDPOINT, VD_INTEGRATION_ENDPOINT,
         CALLBACK_VCS_ENDPOINT,
         LDAP_ADAPTER_ENDPOINT, LDAP_ENDPOINT, PORT_ADDRESS_BOOK_MOCK, DB_POSTGRES_PORT]
SAVING_FOLDER_NAME = 'pcap_dump'


def get_saving_dir():
    begin = os.getcwd().split('uc-test-framework')[0] + 'uc-test-framework/'
    if not os.path.isdir(begin + SAVING_FOLDER_NAME):
        os.mkdir(begin + SAVING_FOLDER_NAME)
    return begin + SAVING_FOLDER_NAME


class PacketCapture(threading.Thread):
    capture = 1

    def __init__(self, test_name, lock, iface='any'):
        threading.Thread.__init__(self)
        self.interface_name = iface
        self.filter_string = 'tcp port ' + ' or tcp port '.join(list(map(str, PORTS)))
        self.file = f'{get_saving_dir()}/{test_name}.pcap'
        self.lock = lock

    def stop(self):
        self.capture = 0

    def run(self):
        capture = pyshark.LiveCapture(interface=self.interface_name, display_filter=self.filter_string,
                                      output_file=self.file)
        try:
            for packet in capture.sniff_continuously():
                if not self.capture:
                    self.LOCK.acquire()
                    capture.close()
                    self.LOCK.release()
                    
            #while not self.stop_while:
            #    pass

        except pyshark.capture.capture.TSharkCrashException:
            self.exited = 1
            print("Capture has crashed")
