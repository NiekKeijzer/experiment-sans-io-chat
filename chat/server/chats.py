import typing
from dataclasses import dataclass, field

if typing.TYPE_CHECKING:
    from chat.connection import Client


@dataclass()
class Channel:
    name: str = 'Lobby'
    clients: list['Client'] = field(default_factory=list)

    def join(self, client: 'Client') -> None:
        if client in self.clients:
            return

        self.clients.append(client)
        client.channel = self

        self.broadcast(f'User {client.alias} joined the channel')

    def leave(self, client: 'Client') -> None:
        if client not in self.clients:
            return

        self.clients.remove(client)
        self.broadcast(f'User {client.alias} left the channel')

    def broadcast(self, message: str, sender: str = 'System'):
        for client in self.clients:
            if client.alias == sender:
                continue

            client.send_message(message, sender)


@dataclass()
class Hub:
    channels: dict[str, Channel] = field(default_factory=dict)
    default_channel: Channel = Channel()

    def join(self, client: 'Client') -> None:
        self.default_channel.join(client)

    def leave(self, client: 'Client') -> None:
        client.channel.leave(client)

    def find_client_channel(self, client) -> Channel:
        for channel in self.channels.values():
            if client not in channel.clients:
                continue

            return channel
        else:
            raise LookupError
