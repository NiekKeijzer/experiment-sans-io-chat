import trio
from chat.connection import Client
from chat.middleware import MiddlewareStack
from chat.protocol.yolo import YoloProtocol


async def main(host: str = '127.0.0.1', port=3331) -> None:
    client = Client(YoloProtocol(), MiddlewareStack())
    print(f'>>> {client.alias}: ping')
    client.send_message('ping')

    stream = await trio.open_tcp_stream(host, port)
    await stream.send_all(client.outgoing())
    message = await stream.receive_some(1024)
    for message in client.handle_incoming(message):
        print(f'<<< {message.sender}: {message.message}')


if __name__ == '__main__':
    try:
        trio.run(main)
    except KeyboardInterrupt:
        print('Bye bye 👋')
