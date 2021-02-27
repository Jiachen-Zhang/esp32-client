"""
消息队列全局变量管理工具类
"""
from queue import Queue

SERIAL_QUEUE: Queue = Queue(maxsize=64)
