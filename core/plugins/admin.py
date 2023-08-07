from pyrogram import Client, filters
from pyrogram.errors.exceptions import PeerIdInvalid
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from core.config import Session
from core.database.models import Admin
from core.utils.custom_filters import check_status, has_status


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
                InlineKeyboardButton("❌", f"admin|remove|{page}|{x['id']}"),
            ]
        )

    page_buttons = []
    has_more_elements = await Admin.filter(
        id__gt=(data[-1]["id"] if data else None)
    ).exists()

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


@Client.on_callback_query(filters.regex(r"^admin\|remove\|(\d+)\|(\d+)$"))
async def remove_admin_cb(client: Client, callback_query: CallbackQuery):
    matches = callback_query.matches[0]
    page = int(matches.group(1))
    admin_id = int(matches.group(2))

    data = await Admin.get_or_none(id=admin_id)

    if not data:
        return await callback_query.answer("Impossibile!")

    await data.delete()

    Session.admins.remove(data.user_id)

    await callback_query.edit_message_reply_markup(
        await get_list_admin(client, page)
    )


@Client.on_callback_query(filters.regex(r"^admin\|add$") & ~has_status)
async def add_admin_cb(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("Now send the id of the new admin:")

    Session.status[callback_query.from_user.id]["status"] = "add_admin"


@Client.on_message(check_status("add_admin") & filters.text)
async def add_admin(client: Client, message: Message):
    del Session.status[message.from_user.id]

    try:
        new_admin_id = int(message.text)
    except ValueError:
        return await message.reply("The text is not a id")

    try:
        await client.get_users(new_admin_id)
    except PeerIdInvalid:
        return await message.reply("The user has not start the bot")

    Session.admins.add(new_admin_id)
    await Admin.create(user_id=new_admin_id)

    await message.reply("Done!")
