import uuid
from dataclasses import dataclass, field
from typing import Generator

from .message import Message
from .middleware import MiddlewareStack
from .protocol._abc import Protocol
from .protocol.errors import ProtocolDecodeError
from .server.chats import Hub, Channel


@dataclass
class Connection:
    protocol: Protocol
    middleware: MiddlewareStack
    _in_buffer: bytearray = field(default_factory=bytearray)
    _out_buffer: bytearray = field(default_factory=bytearray)

    def handle_incoming(self, data: bytes):
        self._in_buffer.extend(data)

        return self.messages

    def outgoing(self) -> bytes:
        outgoing = bytes(self._out_buffer)
        del self._out_buffer[:]

        return outgoing

    @property
    def messages(self) -> Generator[Message, None, None]:
        while True:
            try:
                message = self.protocol.decode(self._in_buffer)
            except ProtocolDecodeError:
                break

            if not message:
                break

            yield message

    def handle_message(self, message: Message) -> None:
        ...

    def send_message(self, message: str, sender: str = 'System') -> None:
        data = self.protocol.encode(Message(message, sender=sender))
        self._out_buffer.extend(data)


@dataclass()
class Client(Connection):
    channel: Channel = None
    alias: str = field(default_factory=uuid.uuid4)

    def handle_message(self, message: Message) -> None:
        message = self.middleware(self, message)

        if self.channel is not None:
            self.channel.broadcast(message.message, self.alias)


@dataclass
class Server(Connection):
    hub: Hub = field(default_factory=Hub)

    def handle_connection(self) -> Client:
        client = Client(self.protocol, self.middleware)
        self.hub.join(client)

        return client
