import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
from dotenv import load_dotenv

from core.config import Config, Session
from core.database import init_db
from core.plugins import load_plugins

load_dotenv()

conf = Session.config = Config()

bot = Bot(conf.BOT_TOKEN)
dp = Dispatcher(bot)
executor = Executor(dp, skip_updates=True)


async def main():
    await init_db()

    load_plugins(dp)

    await executor._startup_polling()
    await dp.start_polling()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(executor._shutdown_polling())
