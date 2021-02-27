"""
test for tcp_client.py
"""
import unittest
from tcp_client import TCPClient


class MyTestCase(unittest.TestCase):
    """
    TCP_Client测试
    """
    def test_flush_queue(self):
        """
        测试清空队列数据
        :return:
        """
        tcp_client = TCPClient()
        result: bool = tcp_client.flush_queue()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
