import functools
import typing

from aiogram.types.base import TelegramObject

from core.utilities import filters


def on_update(type_handler: str, filters: filters = filters.all):
    def decorator(func: typing.Callable):
        func.type_handler = type_handler

        @functools.wraps(func)
        async def wrapper(update: TelegramObject):
            if not (await filters(update)):
                return

            return await func(update)

        return wrapper

    return decorator
