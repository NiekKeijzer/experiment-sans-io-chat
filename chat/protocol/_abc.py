import abc

from chat.message import Message


class Protocol(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self, message: Message) -> bytes:
        ...

    @abc.abstractmethod
    def decode(self, data: bytes) -> Message:
        ...
