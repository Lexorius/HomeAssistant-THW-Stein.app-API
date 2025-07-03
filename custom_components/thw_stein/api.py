
import re, logging, aiohttp
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)
BASE_URL = "https://stein.app"
API_URL  = f"{BASE_URL}/api/api"
JS_RX    = r'<script[^>]+type="module"[^>]+src="([^"]+)"'

class SteinError(RuntimeError):
    pass

class SteinClient:
    def __init__(self, buname: str, *, session: aiohttp.ClientSession):
        self._session, self._buname = session, buname
        self._headers = {}
        self._bu = None

    async def _init_headers(self):
        if self._headers:
            return
        async with self._session.get(BASE_URL) as r:
            html = await r.text()
        m = re.search(JS_RX, html)
        if not m:
            raise SteinError("Script-URL nicht gefunden")
        async with self._session.get(f"{BASE_URL}/{m.group(1)}") as js:
            js_text = await js.text()
        k = re.search(r'["\']X-API-KEY["\']\s*[:=]\s*["\']([A-Za-z0-9]+)["\']', js_text)
        if not k:
            raise SteinError("X-API-KEY not found in JS.")
        self._headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "x-api-key": k.group(1),
        }

    async def login(self, user: str, pwd: str):
        await self._init_headers()
        await self._session.post(f"{API_URL}/login_check", json={"username": user, "password": pwd})
        async with self._session.get(f"{API_URL}/app/data", headers=self._headers) as resp:
            data = await resp.json()
        self._bu = next(bu for bu in data["bus"] if bu["name"].lower() == self._buname.lower())

    async def async_get_assets(self) -> List[Dict[str, Any]]:
        url = f"{API_URL}/assets?buIds={self._bu['id']}"
        async with self._session.get(url, headers=self._headers) as resp:
            return await resp.json()
