from pyrogram import filters
from pyrogram.types import CallbackQuery

from core.config import Session


async def has_status_filter(_, __, query: CallbackQuery):
    return query.from_user.id in Session.status


has_status = filters.create(has_status_filter)


def check_status(data: str):
    async def func(flt, _, query: CallbackQuery):
        if query.from_user.id not in Session.status:
            return False
        return flt.data == Session.status[query.from_user.id]["status"]

    return filters.create(func, data=data)
