import asyncio
import pathlib

from dotenv import load_dotenv
from pyrogram import Client
from tortoise import run_async

from core.config import Config, Session
from core.database import init_db


async def main():
    # Load env
    load_dotenv()

    # Load config
    conf = Session.config = Config()

    # Add owner
    Session.owner.add(conf.OWNER_ID)

    # start db
    await init_db()

    # Create session directory - if not exists
    path = pathlib.Path("core/session")
    path.mkdir(exist_ok=True)

    # Create pyrogram client
    client = Client(
        "shelly-bot",
        conf.API_ID,
        conf.API_HASH,
        bot_token=conf.BOT_TOKEN,
        workdir=path,
        plugins=dict(root="core/plugins"),
    )

    # Start client
    await client.start()

    # idle
    while True:
        await asyncio.sleep(600)


if __name__ == "__main__":
    try:
        run_async(main())
    except KeyboardInterrupt:
        pass
