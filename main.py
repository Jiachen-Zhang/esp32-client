"""
start program for client side application
"""
import _thread
from serial_reader import SerialReader
from tcp_client import TCPClient

SERIAL_PORT = '/dev/tty.usbserial-0001'
BAUD_RATE = 115200
if __name__ == '__main__':
    serial_reader = SerialReader(_serial_port=SERIAL_PORT, _baud_rate=BAUD_RATE)
    _thread.start_new_thread(serial_reader.assembly_serial_data, ())
    tcp_client = TCPClient('127.0.0.1', 5000)
    tcp_client.send_serial_data()
