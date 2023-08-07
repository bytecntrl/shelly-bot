import importlib
import pathlib

from telethon import TelegramClient

PATH = "core.plugins"


def load_plugins(client: TelegramClient):
    path = pathlib.Path(*PATH.split("."))
    plugin_files = list(
        filter(lambda x: not x.name.startswith("_"), path.glob("*.py"))
    )

    for file in plugin_files:
        module = importlib.import_module(f"{PATH}.{file.stem}")

        for v in module.__dict__.values():
            if callable(v) and hasattr(v, "event"):
                client.add_event_handler(v, v.event)
