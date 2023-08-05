import functools
import typing

from aiogram.types.base import TelegramObject


def on_update(type_handler: str):
    def decorator(func: typing.Callable):
        func.type_handler = type_handler

        @functools.wraps(func)
        async def wrapper(update: TelegramObject):
            return await func(update)

        return wrapper

    return decorator
