import os
import typing

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)

LIST_ENV = {
    "BOT_TOKEN": "BOT_TOKEN",
}


class MyCustomSource(EnvSettingsSource):
    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: typing.Any,
        value_is_complex: bool,
    ) -> typing.Any:
        if v := os.environ.get(LIST_ENV.get(field_name) or ""):
            return v
        return value


class Config(BaseSettings):
    # Telegram settings
    BOT_TOKEN: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)
