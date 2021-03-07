"""
从管道读取数据并发送至云函数以日志形式存储
"""
import time
import requests
from utils.logger import log
from utils.channel import SERIAL_QUEUE
from serial_reader import SerialReader


def mock_data(_line: str, num: int) -> list:
    """
    生成测试数据
    """
    _data = []
    for _ in range(num):
        _data.append(_line + ", "+ str(int(time.time()*1000)))
    return _data

TEST_URL = 'https://service-mpkbqc6a-1256776799.gz.apigw.tencentcs.com/test/esp_collector'
RELEASE_URL = 'https://service-mpkbqc6a-1256776799.gz.apigw.tencentcs.com/release/esp_collector'

def post_data(_data: list, post_url=RELEASE_URL):
    """
    将数据以POST请求发送给云函数
    """
    _r = requests.post(url=post_url, json=_data)
    log.info("send %d at %f", _r.status_code, time.time())

# if __name__ == '__main__':
#     data = mock_data('CSI_DATA,AP,A8:03:2A:68:69:BC,-57,11,1,5,1,1,1,1,0,0,0,-91,1,8,1, \
#         5589939,0,84,0,0,5.782990,384,[84 -64 4 0 0 0 0 0 0 0 0 0 0 24 -1 24 -1 24 -3 24 \
#             -3 24 -4 24 -4 23 -5 23 -5 23 -5 23 -5 22 -5 22 -6 21 -6 21 -6 21 -6 20 -6 \
#                 19 -6 19 -5 19 -5 19 -5 19 -5 18 -5 18 -4 18 -3 17 -4 17 0 0 -3 16 -3 \
#                     16 -2 16 -2 16 -1 15 -1 16 0 15 0 15 0 15 0 15 1 14 1 14 2 14 2 14 \
#                         2 14 2 13 3 13 3 13 4 13 4 13 4 12 4 12 5 12 5 11 6 11 5 11 0 \
#                             0 0 0 0 0 0 0 0 0 ]', 1000)
#     start = time.time()
#     post_data(data, TEST_URL)
#     print(time.time() - start)
if __name__ == '__main__':
    import _thread
    SERIAL_PORT = '/dev/tty.usbserial-0001'
    BAUD_RATE = 921600
    serial_reader = SerialReader(_serial_port=SERIAL_PORT, _baud_rate=BAUD_RATE)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    data = []
    MAX_LEN = 1024
    while True:
        line = SERIAL_QUEUE.get()
        # remove \r\n
        data.append(line.strip())
        _len = len(data)
        if _len >= MAX_LEN:
            post_data(data)
            data = []
        elif _len % 100 == 0:
            log.info('%d/%d', _len, MAX_LEN)
