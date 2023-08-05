from aiogram.types import Message

from core.decorators import on_update
from core.utilities import filters


@on_update("message", filters.command(["start"]))
async def start(message: Message):
    await message.reply("Hi!")
