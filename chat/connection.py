import uuid
from dataclasses import dataclass, field
from typing import Generator

from .message import Message
from .protocol._abc import Protocol
from .protocol.errors import ProtocolDecodeError


@dataclass
class Connection:
    protocol: Protocol
    _in_buffer: bytearray = field(default_factory=bytearray)
    _out_buffer: bytearray = field(default_factory=bytearray)

    def handle_incoming(self, data: bytes):
        self._in_buffer.extend(data)

        for message in self.messages:
            self.handle_message(message)

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
                message = False

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
    ...


@dataclass()
class _ServerClient(Connection):
    alias: str = field(default_factory=uuid.uuid4)

    def handle_message(self, message: Message) -> None:
        if message.message.strip() == 'ping':
            self.send_message('pong', self.alias)


@dataclass
class Server(Connection):
    def handle_connection(self) -> _ServerClient:
        # TODO: Keep track of clients somewhere
        client = _ServerClient(self.protocol)

        return client
