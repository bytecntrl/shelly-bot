from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.config import Session

START_BUTTONS_OWNER = (
    ("🛠 Manage Shelly", "shelly|manage|1"),
    ("📊 Status Shelly", "shelly|status|1"),
    ("👮 Admin", "admin|1"),
)

START_BUTTONS_ADMIN = (("📊 Status Shelly", "shelly|status|1"),)


@Client.on_message(filters.command("start") & ~Session.owner & ~Session.admins)
async def start(_: Client, message: Message):
    await message.reply(
        f"hello, you can't use this bot\nyour id: `{message.from_user.id}`"
    )


@Client.on_message(filters.command("start") & Session.admins)
async def start_admin(_: Client, message: Message):
    await message.reply(
        "hi!",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text, callback_data=cb)]
                for text, cb in START_BUTTONS_ADMIN
            ]
        ),
    )


@Client.on_message(filters.command("start") & Session.owner)
async def start_owner(_: Client, message: Message):
    await message.reply(
        "hi!",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text, callback_data=cb)]
                for text, cb in START_BUTTONS_OWNER
            ]
        ),
    )
