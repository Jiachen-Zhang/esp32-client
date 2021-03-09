"""
串口读取模块
负责从串口读取数据并写入管道
"""
import time
from queue import Full
from multiprocessing.connection import Connection
from serial import LF, Serial
from utils.logger import log
from utils.channel import SERIAL_QUEUE


class SerialReader:
    """
    串口读取对象
    """

    def __init__(self,
                 _serial_pipe_sender: Connection = None,
                 _serial_port: str = '/dev/ttyUSB0',
                 _baud_rate: int = 115200, ):
        self.serial_pipe_sender = _serial_pipe_sender
        self._serial_port = _serial_port
        self._baud_rate = _baud_rate
        self.serial = None

    def reset(self):
        """
        刷新串口数据
        :return:
        """
        self.serial.flushInput()

    def __connect(self):
        self.serial = Serial(self._serial_port, self._baud_rate, timeout=3)
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

    def __read_serial_data(self):
        serial_data = self.serial.read_until(expected=LF, size=4096)
        # remove /r/n
        serial_data = self.__append_time(serial_data)
        if not serial_data.startswith('CSI_DATA'):
            log.info(serial_data)
        return serial_data

    def assembly_serial_data(self):
        """
        按行组装串口数据并发送至管道
        :return:
        """
        self.__connect()
        if self.serial_pipe_sender is None:
            while True:
                serial_data = self.__read_serial_data()
                if serial_data == '' or not serial_data.startswith('CSI_DATA'):
                    continue
                assert serial_data.endswith('\n')
                try:
                    SERIAL_QUEUE.put_nowait(serial_data)
                except Full:
                    log.warning('Write Failed to SERIAL_QUEUE [Full]')
        else:
            while True:
                serial_data = self.__read_serial_data()
                if serial_data == '' or not serial_data.startswith('CSI_DATA'):
                    continue
                assert serial_data.endswith('\n')
                self.serial_pipe_sender.send(serial_data)


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
        line: str = SERIAL_PIPE[1].recv()
        line = line.rstrip()
        print('READ: {}'.format(line))
