import trio
from chat.connection import Server
from chat.protocol.yolo import YoloProtocol


async def handle_incoming(server: Server, stream: trio.SocketStream) -> None:
    server_client = server.handle_connection()
    while True:
        try:
            data = await stream.receive_some(1024)
        except trio.BrokenResourceError:
            break

        server_client.handle_incoming(data)

        await stream.send_all(server_client.outgoing())


async def main(host: str = '127.0.0.1', port=3331) -> None:
    server = Server(YoloProtocol())

    await trio.serve_tcp(lambda stream: handle_incoming(server, stream), port, host=host)


if __name__ == '__main__':
    try:
        trio.run(main)
    except KeyboardInterrupt:
        print('Bye bye 👋')
