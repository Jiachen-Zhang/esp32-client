#!/usr/bin/env python3

import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000  # The port used by the server

data = 'CSI_DATA,AP,3C:71:BF:6D:2A:78,-73,11,1,0,1,1,1,0,0,0,0,-93,0,1,1,80272146,0,101,0,0,80.363225,384,[101 -48 5 ' \
       '0 0 0 0 0 0 0 5 2 23 12 25 13 27 16 28 19 27 20 24 22 22 23 20 24 19 25 18 25 20 27 20 27 18 26 16 26 16 25 ' \
       '16 25 14 23 12 21 12 21 12 20 14 19 15 18 14 17 16 17 18 16 18 14 10 6 20 11 20 10 22 10 22 10 23 10 25 11 25 ' \
       '10 24 8 25 7 27 5 27 5 26 6 26 7 27 8 27 7 28 6 29 5 27 4 25 3 25 3 26 4 26 4 26 3 26 3 25 3 24 1 5 0 0 0 0 0 ' \
       '0 0 0 0 ], %d\r\n'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    start = time.time()
    cnt = 0
    print('start send', time.time())
    while True:
        cnt += 1
        msg = data % int(time.time())
        s.sendall(msg.encode('utf-8'))
        time.sleep(0.02)
        # if time.time() - start > 1 or cnt >= 500:
        #     break
    s.close()
    print('total send', time.time(), cnt)


print('Received', repr(data))
