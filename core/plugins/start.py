from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.decorators import on_update
from core.utilities import filters

START_BUTTONS = (
    ("🛠 Manage Shelly", "shelly|manage"),
    ("📊 Status Shelly", "shelly|status"),
    ("👮 Admin", "admin"),
)


@on_update("message", filters.command(["start"]))
async def start(message: Message):
    await message.reply(
        "Hi!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(x[0], callback_data=x[1])]
                for x in START_BUTTONS
            ]
        ),
        reply=False,
    )
