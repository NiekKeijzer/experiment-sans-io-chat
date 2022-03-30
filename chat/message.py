from dataclasses import dataclass


@dataclass
class Message:
    message: str
    sender: str

    @classmethod
    def from_dict(cls, _dict, **kwargs) -> 'Message':
        values = {**_dict, **kwargs}
        message_dict = {}
        for field in cls.__annotations__.keys():
            message_dict[field] = values.get(field)

        return cls(**message_dict)

    def __rich__(self) -> str:
        pass
