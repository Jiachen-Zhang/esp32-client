import time
from serial import LF, Serial
from utils.logger import log
from utils.channel import SERIAL_QUEUE, Full


class SerialReader:

    def __init__(self, _serial_port: str = '/dev/tty.USB0', _baud_rate: int = 115200):
        self.serial = Serial(_serial_port, _baud_rate, timeout=3)
        self.serial.flushInput()

    def assembly_serial_data(self):
        while _data := self.serial.read_until(expected=LF, size=4096):
            log.debug('SERIAL: {}'.format(_data))
            try:
                _data = _data.decode('utf-8')
            except UnicodeDecodeError:
                continue
            _data += ', {}'.format(time.time())
            try:
                SERIAL_QUEUE.put_nowait(_data)
            except Full:
                log.warn('Write Failed to SERIAL_QUEUE [Full]')


if __name__ == '__main__':
    import _thread
    serial_port = '/dev/tty.usbserial-0001'
    baud_rate = 115200
    serial_reader = SerialReader(_serial_port=serial_port, _baud_rate=baud_rate)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    while data := SERIAL_QUEUE.get():
        print('READ: {}'.format(data))
