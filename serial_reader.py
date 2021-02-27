"""
串口读取模块
负责从串口读取数据并写入管道
"""
import time
from queue import Full
from serial import LF, Serial
from utils.logger import log
from utils.channel import SERIAL_QUEUE


class SerialReader:
    """
    串口读取对象
    """

    def __init__(self, _serial_port: str = '/dev/tty.USB0', _baud_rate: int = 115200):
        self.serial = Serial(_serial_port, _baud_rate, timeout=3)
        self.serial.flushInput()

    def reset(self):
        """
        刷新串口数据
        :return:
        """
        self.serial.flushInput()

    @staticmethod
    def __append_time(serial_data: bytes) -> str:
        """
        remove \r\n and append timestamp to end of line
        :param serial_data:
        :return:
        """
        serial_data = serial_data[:-2]
        log.debug('SERIAL: %s', serial_data)
        try:
            _data: str = serial_data.decode('utf-8')
        except UnicodeDecodeError:
            return ''
        _data += ', {}\n'.format(time.time())
        return _data

    def assembly_serial_data(self):
        """
        按行组装串口数据并发送至管道
        :return:
        """
        while True:
            serial_data = self.serial.read_until(expected=LF, size=4096)
            # remove /r/n
            serial_data = self.__append_time(serial_data)
            print(serial_data, end='')
            if serial_data == '' or not serial_data.startswith('CSI_DATA'):
                continue
            assert serial_data.endswith('\n')
            try:
                SERIAL_QUEUE.put_nowait(serial_data)
            except Full:
                log.warning('Write Failed to SERIAL_QUEUE [Full]')


if __name__ == '__main__':
    import _thread
    SERIAL_PORT = '/dev/tty.usbserial-0001'
    BAUD_RATE = 115200
    serial_reader = SerialReader(_serial_port=SERIAL_PORT, _baud_rate=BAUD_RATE)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    while data := SERIAL_QUEUE.get():
        print('READ: {}'.format(data), end='')
