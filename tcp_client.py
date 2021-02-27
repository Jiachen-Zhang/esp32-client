#!/usr/bin/env python3
"""
TCP客户端，用于将串口数据发送至服务端
"""
import time
from queue import Full
from socket import socket, AF_INET, SOCK_STREAM
from utils.logger import log
from utils.channel import SERIAL_QUEUE


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000  # The port used by the server


class TCPClient:
    """
    TCP客户端对象
    """

    def __init__(self, server_host: str = '127.0.0.1', server_port: int = 5000):
        self.server_host: str = server_host
        self.server_port: int = server_port

    def __try_connect(self):
        """
        尝试连接 socket 并忽略连接错误
        :return:
        """
        _s = socket(AF_INET, SOCK_STREAM)
        try:
            _s.connect((self.server_host, self.server_port))
        except ConnectionRefusedError:
            pass
        return _s

    def send_serial_data(self):
        """
        从队列中读取组装好的串口数据并通过TCP socket 发送给服务端
        :return:
        """
        _s = self.__try_connect()
        while True:
            serial_data = SERIAL_QUEUE.get()
            assert isinstance(serial_data, str), 'wrong type of data read from SERIAL_QUEUE'
            _data: bytes = serial_data.encode('utf-8')
            assert _data.endswith(b'\n')
            try:
                _s.sendall(_data)
            except BrokenPipeError:
                log.warning('BrokenPipeError when sending to server SERIAL_QUEUE.qsize() = %d',
                            SERIAL_QUEUE.qsize())
                _s = self.__try_connect()

    @staticmethod
    def flush_queue():
        """
        清除队列缓冲的所有消息
        :return:
        """
        while not SERIAL_QUEUE.empty():
            SERIAL_QUEUE.get_nowait()
        return True


if __name__ == '__main__':
    import _thread
    from threading import Timer

    data: str = 'CSI_DATA,AP,3C:71:BF:6D:2A:78,-73,11,1,0,1,1,1,0,0,0,0,-93,0,1,1,80272146,0,101,' \
                '0,0,80.363225,384,[99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 ' \
                '99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 ' \
                '99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 ' \
                '99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 99 0 ' \
                '99 0 99 0 99 0 99 0], {}\n '
    tcp_client = TCPClient()
    _thread.start_new_thread(tcp_client.send_serial_data, ())

    def produce_data(_num: int, _batch: int = 50):
        """
        模拟数据产生，向管道写入50条数据
        :return:
        """
        log.info('produce_data %f', time.time())
        for _ in range(_batch):
            try:
                _num += 1
                val: str = str(_num)  # str(int(sin(num/30.0) * 50 + 50))
                _data = data.replace('99', val)
                SERIAL_QUEUE.put_nowait(_data.format(time.time()))
                time.sleep(0.015)
                log.info('val = %s', val)
            except Full:
                log.warning('Write Failed to SERIAL_QUEUE [Full]')

    NUM = 0
    BATCH = 50
    while producer_timer := Timer(interval=1, function=produce_data, args=(NUM, BATCH)):
        producer_timer.start()
        producer_timer.join()
        NUM += BATCH
