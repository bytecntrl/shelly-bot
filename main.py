import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

from core.config import Config, Session
from core.plugins.start import start


load_dotenv()

conf = Session.config = Config()

bot = Bot(conf.BOT_TOKEN)
dp = Dispatcher(bot)
executor = Executor(dp, skip_updates=True)


async def main():
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
