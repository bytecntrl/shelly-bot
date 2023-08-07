from telethon import events

from core.decorators import on_update


@on_update(events.NewMessage(pattern="/start"))
async def start(e: events.NewMessage.Event):
    await e.reply("hi!")
