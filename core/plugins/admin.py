from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.errors.exceptions import PeerIdInvalid

from core.config import Session
from core.database.models import Admin


async def get_list_admin(client: Client, page: int):
    limit = Session.config.MAX_ELEMENTS_PAGE
    data = await Admin.all().offset((page - 1) * limit).limit(limit).values()
    result = []

    for x in data:
        try:
            name = (await client.get_users(x["user_id"])).first_name
        except PeerIdInvalid:
            name = x["user_id"]

        result.append(
            [
                InlineKeyboardButton(name, "XX"),
                InlineKeyboardButton("❌", f"admin|remove|{x['id']}"),
            ]
        )

    page_buttons = []
    has_more_elements = await Admin.filter(id__gt=data[-1]["id"]).exists()

    if page > 1:
        page_buttons.append(InlineKeyboardButton("⬅️", f"admin|{page - 1}"))

    if has_more_elements:
        page_buttons.append(InlineKeyboardButton("➡️", f"admin|{page + 1}"))

    result.append([InlineKeyboardButton("➕", "admin|add")])

    if page_buttons:
        result.append(page_buttons)

    return InlineKeyboardMarkup(result)


@Client.on_callback_query(filters.regex(r"^admin\|(\d+)$") & Session.owner)
async def admin_cb(client: Client, callback_query: CallbackQuery):
    page = int(callback_query.matches[0].group(1))

    await callback_query.edit_message_text(
        "List of admin:", reply_markup=await get_list_admin(client, page)
    )
