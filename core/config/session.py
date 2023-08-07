import collections

from aiohttp import ClientSession
from pyrogram import filters

from core.config import Config


class Session:
    config: Config
    owner = filters.user()
    admins = filters.user()
    status: dict[int, dict] = collections.defaultdict(dict)
    session = ClientSession()
