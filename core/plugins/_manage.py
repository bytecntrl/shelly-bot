import importlib
import pathlib

from aiogram import Dispatcher

PATH = "core.plugins"
TYPE_HANDLER = {
    "message": lambda x: x.register_message_handler,
    "callback_query": lambda x: x.register_callback_query_handler,
}


def load_plugins(dp: Dispatcher):
    path = pathlib.Path(*PATH.split("."))
    plugin_files = list(
        filter(lambda x: not x.name.startswith("_"), path.glob("*.py"))
    )

    for file in plugin_files:
        module = importlib.import_module(f"{PATH}.{file.stem}")

        for v in module.__dict__.values():
            if callable(v) and hasattr(v, "type_handler"):
                TYPE_HANDLER[v.type_handler](dp)(v)
