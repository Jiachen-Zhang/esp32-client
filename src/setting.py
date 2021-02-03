#!../venv/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from serial import Serial
from serial.serialutil import SerialException
from os import path

"""
用于初始化项目配置
"""
CFG_PATH = './etc/config.ini'
SERIAL_PORT = None
SEND_BATCH = None
BAUD_RATE = None
POST_URL = None
SERIAL = None

def __load_config() -> ConfigParser:
    print("-*- load config -*- ")
    cfg = ConfigParser()
    if (len(cfg.read(CFG_PATH)) == 0):
        print('No configuration files at', CFG_PATH)
        exit(-1)
    global SERIAL_PORT, SEND_BATCH, BAUD_RATE, POST_URL
    SERIAL_PORT = cfg.get('client', 'serial_port')
    BAUD_RATE = cfg.getint('client', 'baud_rate')
    SEND_BATCH = cfg.getint('client', 'send_batch')
    POST_URL = cfg.get('server', 'post_url')
    return cfg

def __init_serial():
    print('-*- init serial -*-')
    global SERIAL
    if (not path.isfile(SERIAL_PORT)):
        print('Cannot open such serial port, please check your config.ini')
        print('You can run `ls /dev/tty*` to find the correct device port')
        exit(-1)
    SERIAL = Serial(SERIAL_PORT, BAUD_RATE, timeout=3)
    SERIAL.flushInput()

def __init__():
    print("-*- init settings -*- ")
    __load_config()
    __init_serial()
    print("-*- init settings -*- ")
        