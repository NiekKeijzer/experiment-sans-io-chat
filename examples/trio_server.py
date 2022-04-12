import trio
from chat.connection import Server, Client
from chat.middleware import MiddlewareStack
from chat.middleware.ping import ping
from chat.protocol.errors import ProtocolDecodeError
from chat.protocol.yolo import YoloProtocol


async def reader(server_client: Client, stream: trio.SocketStream, server: Server):
    while True:
        try:
            data = await stream.receive_some(1024)
        except trio.BrokenResourceError:
            server.hub.leave(server_client)

            break

        try:
            messages = server_client.handle_incoming(data)
        except ProtocolDecodeError:
            break

        for message in messages:
            server_client.handle_message(message)


async def writer(server_client: Client, stream: trio.SocketStream):
    while True:
        await stream.send_all(server_client.outgoing())


async def handle_incoming(server: Server, stream: trio.SocketStream) -> None:
    server_client = server.handle_connection()
    async with trio.open_nursery() as nursery:
        nursery.start_soon(reader, server_client, stream, server)
        nursery.start_soon(writer, server_client, stream)


async def main(host: str = '127.0.0.1', port=3331) -> None:
    server = Server(YoloProtocol(), MiddlewareStack([ping]))

    await trio.serve_tcp(lambda stream: handle_incoming(server, stream), port, host=host)


if __name__ == '__main__':
    try:
        trio.run(main)
    except KeyboardInterrupt:
        print('Bye bye 👋')
