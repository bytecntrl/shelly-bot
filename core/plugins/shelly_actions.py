from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from core.config import Session
from core.database.models import Shelly
from core.utils import ShellyApi


async def get_action_buttons(page: int):
    limit = Session.config.MAX_ELEMENTS_PAGE
    data = await Shelly.all().offset((page - 1) * limit).limit(limit).values()
    buttons = []

    for x in data:
        api = ShellyApi(x["url"])
        is_active = await api.is_active()

        if not is_active:
            buttons.append(
                [
                    InlineKeyboardButton(x["name"], "XX"),
                ]
            )
        else:
            buttons.append(
                [
                    InlineKeyboardButton(x["name"], "XX"),
                    InlineKeyboardButton(
                        "▶️", f"shelly|actions|open|{x['id']}"
                    ),
                ]
            )

    page_buttons = []
    has_more_elements = await Shelly.filter(
        id__gt=(data[-1]["id"] if data else None)
    ).exists()

    if page > 1:
        page_buttons.append(
            InlineKeyboardButton("⬅️", f"shelly|actions|{page - 1}")
        )

    if has_more_elements:
        page_buttons.append(
            InlineKeyboardButton("➡️", f"shelly|actions|{page + 1}")
        )

    if page_buttons:
        buttons.append(page_buttons)

    return InlineKeyboardMarkup(buttons)


@Client.on_callback_query(
    filters.regex(r"^shelly\|actions\|(\d+)$")
    & (Session.owner | Session.admins)
)
async def shelly_action_cb(_: Client, callback_query: CallbackQuery):
    page = int(callback_query.matches[0].group(1))

    await callback_query.edit_message_text(
        "Shelly actions:", reply_markup=await get_action_buttons(page)
    )
