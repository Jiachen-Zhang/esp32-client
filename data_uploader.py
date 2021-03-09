"""
从管道读取数据并发送至云函数以日志形式存储
"""
import time
import requests
from utils.logger import log
from serial_reader import SerialReader


def mock_data(_line: str, num: int) -> list:
    """
    生成测试数据
    """
    _data = []
    for _ in range(num):
        _data.append(_line + ", " + str(int(time.time() * 1000)))
    return _data


TEST_URL = 'https://service-mpkbqc6a-1256776799.gz.apigw.tencentcs.com/test/esp_collector'
RELEASE_URL = 'https://service-mpkbqc6a-1256776799.gz.apigw.tencentcs.com/release/esp_collector'


def post_data(_data: list, post_url=RELEASE_URL):
    """
    将数据以POST请求发送给云函数
    """
    _r = requests.post(url=post_url, json=_data)
    log.info("send %d at %f", _r.status_code, time.time())


if __name__ == '__main__':
    from multiprocessing.connection import Pipe
    from multiprocessing import Process

    SERIAL_PIPE = Pipe()
    serial_reader = SerialReader(_serial_pipe_sender=SERIAL_PIPE[0],
                                 _serial_port='/dev/tty.usbserial-0001',
                                 _baud_rate=921600)
    p = Process(target=serial_reader.assembly_serial_data,
                args=())
    p.start()
    data = []
    MAX_LEN = 1024
    while True:
        line = SERIAL_PIPE[1].recv()
        # remove \r\n
        data.append(line.strip())
        LEN = len(data)
        if LEN >= MAX_LEN:
            post_data(data)
            data = []
        elif LEN % 100 == 0:
            log.info('%d/%d', LEN, MAX_LEN)
