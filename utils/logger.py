"""
全局日志配置工具
"""
import logging


def get_logger(name: str):
    """
    为调用方生成自定义名称的日志对象
    :param name:
    :return:
    """
    print('init logger')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s %(filename)s[:%(lineno)d]',
                        datefmt='%H:%M:%S')
    return logging.getLogger(name)


log = get_logger(__name__)
