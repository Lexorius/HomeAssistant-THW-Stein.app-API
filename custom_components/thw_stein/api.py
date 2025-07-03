"""Async wrapper for the unofficial Stein.APP API using aiohttp."""
from __future__ import annotations
import re, logging, aiohttp
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)
BASE_URL = "https://stein.app"
API_URL  = f"{BASE_URL}/api/api"
JS_RX    = r'<script[^>]+type="module"[^>]+src="([^\"]+)"'

class SteinError(RuntimeError):
    pass

class SteinClient:
    def __init__(self, buname: str, *, session: aiohttp.ClientSession):
        self._session, self._buname = session, buname
        self._headers: dict[str, str] = {}
        self._bu: dict[str, Any] | None = None

    async def _init_headers(self) -> None:
        if self._headers:
            return
        async with self._session.get(BASE_URL) as r:
            html = await r.text()
        m = re.search(JS_RX, html)
        if not m:
            raise SteinError("JS file not found in Stein front page.")
        async with self._session.get(f"{BASE_URL}/{m.group(1)}") as js_resp:
            js_text = await js_resp.text()
        k = re.search(r'headers\.common\["X-API-KEY"\]\s*=\s*"(\w+)"', js_text)
        if not k:
            raise SteinError("X-API-KEY not found in JS.")
        self._headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "x-api-key": k.group(1),
        }

    async def login(self, user: str, pwd: str) -> None:
        await self._init_headers()
        await self._session.post(f"{API_URL}/login_check", json={"username": user, "password": pwd})
        async with self._session.get(f"{API_URL}/app/data", headers=self._headers) as resp:
            data = await resp.json()
        self._bu = next(bu for bu in data["bus"] if bu["name"].lower() == self._buname.lower())

    async def async_get_assets(self) -> List[Dict[str, Any]]:
        url = f"{API_URL}/assets?buIds={self._bu['id']}"
        async with self._session.get(url, headers=self._headers) as resp:
            return await resp.json()

STATUS_MAP = {
    "ready": "Einsatzbereit",
    "semiready": "Bedingt einsatzbereit",
    "notready": "Nicht einsatzbereit",
    "inuse": "Im Einsatz",
    "maint": "In Wartung",
}