from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from tortoise.exceptions import IntegrityError

from core.config import Session
from core.database.models import Shelly
from core.utils.custom_filters import check_status, has_status


async def get_shelly_buttons(page: int):
    limit = Session.config.MAX_ELEMENTS_PAGE
    data = await Shelly.all().offset((page - 1) * limit).limit(limit).values()
    buttons = [
        [
            InlineKeyboardButton(x["name"], f"XX"),
            InlineKeyboardButton(
                "❌", f"shelly|manage|remove|{page}|{x['id']}"
            ),
        ]
        for x in data
    ]

    page_buttons = []
    has_more_elements = await Shelly.filter(
        id__gt=(data[-1]["id"] if data else None)
    ).exists()

    if page > 1:
        page_buttons.append(
            InlineKeyboardButton("⬅️", f"shelly|manage|{page - 1}")
        )

    if has_more_elements:
        page_buttons.append(
            InlineKeyboardButton("➡️", f"shelly|manage|{page + 1}")
        )

    buttons.append([InlineKeyboardButton("➕", "shelly|manage|add")])

    if page_buttons:
        buttons.append(page_buttons)

    return InlineKeyboardMarkup(buttons)


@Client.on_callback_query(
    filters.regex(r"^shelly\|manage\|(\d+)$") & Session.owner
)
async def shelly_manage_cb(_: Client, callback_query: CallbackQuery):
    page = int(callback_query.matches[0].group(1))

    await callback_query.edit_message_text(
        "List of shelly:", reply_markup=await get_shelly_buttons(page)
    )


@Client.on_callback_query(
    filters.regex(r"^shelly\|manage\|remove\|(\d+)\|(\d+)$") & Session.owner
)
async def remove_shelly_cb(_: Client, callback_query: CallbackQuery):
    matches = callback_query.matches[0]
    page = int(matches.group(1))
    shelly_id = int(matches.group(2))

    data = await Shelly.get_or_none(id=shelly_id)

    if not data:
        return await callback_query.answer("Impossible!")

    await data.delete()

    await callback_query.edit_message_reply_markup(
        await get_shelly_buttons(page)
    )


@Client.on_callback_query(
    filters.regex(r"^shelly\|manage\|add$") & ~has_status & Session.owner
)
async def add_shelly_cb(_: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(
        "Now send the name of the new shelly:"
    )

    Session.status[callback_query.from_user.id]["status"] = "add_shelly"


@Client.on_message(check_status("add_shelly") & filters.text & Session.owner)
async def add_shelly_name(_: Client, message: Message):
    Session.status[message.from_user.id]["name"] = message.text
    Session.status[message.from_user.id]["status"] = "add_shelly_url"

    await message.reply("Now send the url of the new shelly:")


@Client.on_message(
    check_status("add_shelly_url") & filters.text & Session.owner
)
async def add_shelly_url(_: Client, message: Message):
    data = Session.status[message.from_user.id].copy()
    del Session.status[message.from_user.id]

    url = [
        message.text[x.offset : x.offset + x.length]
        for x in message.entities
        if x.type == MessageEntityType.URL
    ]

    if not url:
        return await message.reply("The text is not a URL valid.")

    try:
        await Shelly.create(name=data["name"], url=url[0])
    except IntegrityError:
        return await message.reply("Shelly already exist")

    await message.reply("Done!")
