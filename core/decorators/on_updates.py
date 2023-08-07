import functools
import typing

from telethon import events
from telethon.events.common import EventCommon


def on_update(event: events = events.Raw()):
    def decorator(func: typing.Callable):
        func.event = event

        @functools.wraps(func)
        async def wrapper(update: EventCommon):
            return await func(update)

        return wrapper

    return decorator
