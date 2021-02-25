import time
from serial import LF, Serial
from utils.logger import log
from utils.channel import SERIAL_QUEUE, Full


class SerialReader:

    def __init__(self, _serial_port: str = '/dev/tty.USB0', _baud_rate: int = 115200):
        self.serial = Serial(_serial_port, _baud_rate, timeout=3)
        self.serial.flushInput()

    @staticmethod
    def __append_time(serial_data: bytes) -> str:
        """
        remove \r\n and append timestamp to end of line
        :param serial_data:
        :return:
        """
        serial_data = serial_data[:-2]
        log.debug('SERIAL: {}'.format(serial_data))
        try:
            _data: str = serial_data.decode('utf-8')
        except UnicodeDecodeError:
            return ''
        _data += ', {}\n'.format(time.time())
        return _data

    def assembly_serial_data(self):
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
                log.warn('Write Failed to SERIAL_QUEUE [Full]')


if __name__ == '__main__':
    import _thread
    serial_port = '/dev/tty.usbserial-0001'
    baud_rate = 115200
    serial_reader = SerialReader(_serial_port=serial_port, _baud_rate=baud_rate)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    while data := SERIAL_QUEUE.get():
        print('READ: {}'.format(data), end='')
