from typing import Optional

from chat.message import Message
from ._abc import Protocol
from .errors import ProtocolDecodeError


class YoloProtocol(Protocol):
    def decode(self, data: bytearray) -> Optional[Message]:
        if not data:
            return

        try:
            msg = data.decode()
        except UnicodeDecodeError as e:
            raise ProtocolDecodeError() from e
        del data[:]

        return Message(message=msg, sender='¯\\\_(ツ)_/¯')

    def encode(self, message: Message) -> bytes:
        return message.message.encode()
