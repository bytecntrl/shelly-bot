import pathlib

from telethon import TelegramClient
from dotenv import load_dotenv

from core.config import Config, Session
from core.database import init_db
from core.plugins import load_plugins

load_dotenv()

conf = Session.config = Config()

path = pathlib.Path("core/session")
path.mkdir(exist_ok=True)

client = TelegramClient("core/session/shelly-bot", conf.API_ID, conf.API_HASH)


async def main():
    await init_db()

    load_plugins(client)


if __name__ == "__main__":
    client.start(conf.BOT_TOKEN)
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
