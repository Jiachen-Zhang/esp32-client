import time
import aiohttp
import asyncio
import serial
import time
import collections


SERIAL_PORT = '/dev/tty.usbserial-130'
POST_URL = 'http://192.168.31.5:5000/api/v1/csi/items'
SEND_BATCH = 10
BAUD_RATE = 115200
headers = {'content-type': 'application/json'}
buffer = ""


def __init__():
    print('init serial')
    _serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=3)
    _serial.flushInput()
    print('setup serial')
    return _serial

async def main(json):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(POST_URL, headers=headers, json=json) as res:
                print(res.status)
                print(await res.text())
    except aiohttp.client_exceptions.ClientConnectorError:
        print('Server Not Availible')
    except Exception:
        print('Exception when sending data')

def convert_recv(recv):
    """
    convert received serial data into list of formatted CSI data
    send serial data line by line
    """
    global buffer
    timestamp = time.time()
    data = (buffer + recv).split('\r\n')
    buffer = data[-1]
    data = data[:-1]
    return [{'time': timestamp, 'csi': csi} for csi in data]



if __name__ == '__main__':
    json = {'timestamp': time.time(),
            'data': []}
    _serial = __init__()
    loop = asyncio.get_event_loop()
    while True:
        buffer_count = _serial.inWaiting()
        if buffer_count > 0:
            recv = _serial.read(_serial.in_waiting).decode('utf-8')
            json['data'].extend(convert_recv(recv))
            print(time.time(), '---- recv ----', recv)
        if len(json['data']) >= SEND_BATCH:
            json['timestamp'] = time.time()
            task = loop.create_task(main(json))
            loop.run_until_complete(task)
            json['data'] = []
        time.sleep(0.1)



