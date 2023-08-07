import collections

from pyrogram import filters

from core.config import Config


class Session:
    config: Config
    owner = filters.user()
    admins = filters.user()
    status: dict[int, dict] = collections.defaultdict(dict)
