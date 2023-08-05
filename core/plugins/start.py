from aiogram.types import Message

from core.decorators import on_update


@on_update("message")
async def start(message: Message):
    await message.reply("AA")
