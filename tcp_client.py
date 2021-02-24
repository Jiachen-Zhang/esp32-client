#!/usr/bin/env python3
import time
from utils.channel import SERIAL_QUEUE
from socket import socket, AF_INET, SOCK_STREAM
from utils.logger import log

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000  # The port used by the server


class TCPClient:

    def __init__(self, server_host: str = '127.0.0.1', server_port: int = 5000):
        self.server_host: str = server_host
        self.server_port: int = server_port

    def __connect(self):
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((self.server_host, self.server_port))
        except ConnectionRefusedError:
            pass
        return s

    def send_serial_data(self):
        s = self.__connect()
        while serial_data := SERIAL_QUEUE.get():
            assert isinstance(serial_data, str), 'wrong type of data read from SERIAL_QUEUE'
            _data: bytes = serial_data.encode('utf-8')
            assert _data.endswith(b'\n')
            try:
                s.sendall(_data)
            except BrokenPipeError:
                log.warn('BrokenPipeError when sending to server SERIAL_QUEUE.qsize() = {}'
                         .format(SERIAL_QUEUE.qsize()))
                s = self.__connect()


if __name__ == '__main__':
    import _thread
    from queue import Full
    data = 'CSI_DATA,AP,3C:71:BF:6D:2A:78,-73,11,1,0,1,1,1,0,0,0,0,-93,0,1,1,80272146,0,101,0,0,80.363225,384,' \
           '[101 -48 5 0 0 0 0 0 0 0 5 2 23 12 25 13 27 16 28 19 27 20 24 22 22 23 20 24 19 25 18 25 20 27 20 27 18 ' \
           '26 16 26 16 25 16 25 14 23 12 21 12 21 12 20 14 19 15 18 14 17 16 17 18 16 18 14 10 6 20 11 20 10 22 10 ' \
           '22 10 23 10 25 11 25 10 24 8 25 7 27 5 27 5 26 6 26 7 27 8 27 7 28 6 29 5 27 4 25 3 25 3 26 4 26 4 26 3 ' \
           '26 3 25 3 24 1 5 0 0 0 0 0 0 0 0 0 ], {}\n'
    tcp_client = TCPClient()
    _thread.start_new_thread(tcp_client.send_serial_data, ())
    while True:
        try:
            SERIAL_QUEUE.put_nowait(data.format(time.time()))
        except Full:
            pass
        time.sleep(0.01)
