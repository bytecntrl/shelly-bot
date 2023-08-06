import re
import pathlib

from tortoise import Tortoise

from core.database import models

HAS_SNAKE_CASE: str = "^[a-z]+(_[a-z]+)*$"


def is_snake_case(data: str) -> bool:
    return bool(re.search(HAS_SNAKE_CASE, data))


async def init_db():
    path = pathlib.Path("data")
    path.mkdir(exist_ok=True)

    await Tortoise.init(
        db_url="sqlite://data/db.sqlite",
        modules={
            "models": list(
                map(
                    lambda x: f"core.database.models.{x}",
                    filter(is_snake_case, dir(models)),
                )
            )
        },
        timezone="Europe/Rome",
    )
    await Tortoise.generate_schemas()
