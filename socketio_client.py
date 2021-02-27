"""
socket.io 传输数据 demo
"""
import asyncio
import socketio


sio = socketio.AsyncClient()



@sio.event
async def connect():
    """
    连接
    :return:
    """
    print('connection established')

    await sio.emit('csi_amplitude', 'ping')


@sio.event
async def chat_message(data):
    """
    聊天消息
    :param data:
    :return:
    """
    print('message received with ', data)
    # await sio.emit('chat_message', 'ping')


@sio.event
async def csi_amplitude(date):
    """
    CSI幅度数据
    :param date:
    :return:
    """
    print('received: {}'.format(date))


@sio.event
async def disconnect():
    """
    断开连接
    :return:
    """
    print('disconnected from server')


async def main():
    """
    主函数
    :return:
    """
    await sio.connect('http://localhost:5005')
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
