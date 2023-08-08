import asyncio

from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel, ValidationError

from core.config import Session


class GetShellyResponse(BaseModel):
    type: str
    mac: str
    auth: bool
    fw: str
    longid: int


class ShellyApi:
    def __init__(self, url: str) -> None:
        self.url = url

        if not url.startswith("http://") and not url.startswith("https://"):
            self.url = f"http://{url}"

        if not self.url.endswith("/"):
            self.url = f"{self.url}/"

    async def is_active(self) -> bool:
        try:
            async with Session.session.get(f"{self.url}shelly") as resp:
                status = await resp.json()

                return bool(resp.status == 200 and GetShellyResponse(**status))
        except (ClientError, asyncio.TimeoutError, ValidationError):
            return False

    async def turn_on(self) -> bool:
        params = {"turn": "toggle"}

        try:
            async with Session.session.get(
                f"{self.url}relay/0", params=params
            ) as resp:
                relay = await resp.json()

                return bool(resp.status == 200 and "ison" in relay)
        except (ClientError, asyncio.TimeoutError):
            return False

    async def is_on(self) -> bool | None:
        try:
            async with Session.session.get(f"{self.url}relay/0") as resp:
                relay = await resp.json()

                if not (resp.status == 200 and "ison" in relay):
                    return None

                return relay["ison"]
        except (ClientError, asyncio.TimeoutError):
            return None
