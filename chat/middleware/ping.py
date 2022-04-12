from typing import Callable, Any

from chat.connection import Connection
from chat.message import Message


def ping(connection: Connection, message: Message, call_next: Callable[[Message], Any]) -> Any:
    if message.message.strip() == 'ping':
        connection.send_message('pong')

    return call_next(message)
