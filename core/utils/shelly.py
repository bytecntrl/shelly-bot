from aiohttp.client_exceptions import ClientError

from core.config import Session


class ShellyApi:
    def __init__(self, url: str) -> None:
        self.url = url

        if not url.startswith("http://") and not url.startswith("https://"):
            self.url = f"http://{url}"

        if not self.url.endswith("/"):
            self.url = f"{self.url}/"

    async def is_active(self) -> bool:
        try:
            async with Session.session.get(f"{self.url}status") as resp:
                status = await resp.json()

                return (
                    resp.status == 200
                    and "wifi_sta" in status
                    and status["wifi_sta"]["connected"]
                )
        except ClientError:
            return False

    async def get_name(self) -> str | None:
        try:
            async with Session.session.get(f"{self.url}settings") as resp:
                settings = await resp.json()

                if resp.status == 200 and "name" in settings:
                    return settings["name"]

                return
        except ClientError:
            return
