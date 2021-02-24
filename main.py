import _thread
from serial_reader import SerialReader
from utils.channel import SERIAL_QUEUE


if __name__ == '__main__':
    serial_port = '/dev/tty.usbserial-0001'
    baud_rate = 115200
    serial_reader = SerialReader(_serial_port=serial_port, _baud_rate=baud_rate)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    while data := SERIAL_QUEUE.get():
        print('READ: {}'.format(data))