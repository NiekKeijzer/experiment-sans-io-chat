from dataclasses import dataclass, field
from typing import Callable, Any
from functools import reduce


@dataclass()
class MiddlewareStack:
    """
    Usage:

    >>> def foo(msg, next):
    >>>     print("Called foo")
    >>>
    >>>     return next(msg)
    >>>
    >>>
    >>> def bar(msg, next):
    >>>     print("Called bar")
    >>>
    >>>     return next(msg)
    >>>
    >>>
    >>> def handler(msg):
    >>>     print(msg)
    >>>
    >>> stack = MiddlewareStack(middlewares=[
    >>>     foo, bar
    >>> ])
    >>> stack("Hello World!")
    """
    middlewares: list[Callable] = field(default_factory=list)

    def __call__(self, *args, **kwargs):
        stack = self.build_stack(lambda msg: msg, self.middlewares)

        return stack(*args, **kwargs)

    @classmethod
    def build_stack(cls, func: Callable, middlewares: list[Callable[[Any, ...], None]]):
        return reduce(
            lambda acc, m: lambda *args: m(*args, acc),
            reversed(middlewares),
            lambda *args: func(*args),
        )
