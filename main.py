import _thread
from serial_reader import SerialReader
from tcp_client import TCPClient


if __name__ == '__main__':
    serial_port = '/dev/tty.usbserial-0001'
    baud_rate = 115200
    serial_reader = SerialReader(_serial_port=serial_port, _baud_rate=baud_rate)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    tcp_client = TCPClient('127.0.0.1', 5000)
    tcp_client.send_serial_data()
