import json
import struct
from dataclasses import asdict
from typing import Optional

from chat.message import Message
from ._abc import Protocol
from .errors import ProtocolDecodeError


class JsonProtocol(Protocol):
    def decode(self, data: bytearray) -> Optional[Message]:
        if len(data) < 4:
            return

        msg_length = struct.unpack(">I", data[:4])[0]
        del data[:4]

        if len(data) < msg_length:
            # Wait for more data
            return

        raw_msg = data[:msg_length]
        del data[:msg_length]

        try:
            msg_data = json.loads(raw_msg)
        except json.JSONDecodeError as e:
            raise ProtocolDecodeError from e

        return Message.from_dict(msg_data)

    def encode(self, message: Message) -> bytes:
        try:
            msg_data = json.dumps(asdict(message)).encode()
        except json.JSONDecodeError as e:
            raise ProtocolDecodeError from e

        return struct.pack('>I', len(msg_data)) + msg_data
