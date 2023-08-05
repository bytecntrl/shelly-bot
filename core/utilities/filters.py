from aiogram.types import Message
from aiogram.types.base import TelegramObject
from aiogram.types.chat import ChatType
from aiogram.types.message_entity import MessageEntityType


class Filter:
    async def __call__(self, update: TelegramObject):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    async def __call__(self, update: TelegramObject):
        x = await self.base(update)

        return not x


class AndFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, update: TelegramObject):
        x = await self.base(update)
        y = await self.other(update)

        return x and y


class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, update: TelegramObject):
        x = await self.base(update)
        y = await self.other(update)

        return x or y


class _All(Filter):
    async def __call__(self, _: TelegramObject) -> bool:
        return True


all = _All()


class _Private(Filter):
    async def __call__(self, update: Message) -> bool:
        return bool(update.effective_chat.type == ChatType.PRIVATE)


private = _Private()


class command(Filter):
    def __init__(self, commands: list[str], prefix: str = "/") -> None:
        self.commands = commands
        self.prefix = prefix

    async def __call__(self, update: Message):
        if not update.text:
            return False

        command = [
            update.text[0 : x.length]
            for x in update.entities
            if x.offset == 0
            if x.type
            in (
                MessageEntityType.BOT_COMMAND,
                MessageEntityType.MENTION,
            )
        ]

        if not command:
            return False

        command = command[0].replace(
            f"@{(await update.bot.get_me()).username}", ""
        )

        return any(
            map(
                lambda x: f"{self.prefix}{x}" == command,
                self.commands,
            )
        )
