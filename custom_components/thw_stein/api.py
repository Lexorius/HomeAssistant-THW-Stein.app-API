"""Async-Wrapper um die (inoffizielle) Stein.APP-API."""
from __future__ import annotations
import re, logging, httpx
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)
BASE_URL = "https://stein.app"
API_URL  = f"{BASE_URL}/api/api"
JS_RX    = r'headers\.common\["X-API-KEY"]="(\w+)"'

class SteinError(RuntimeError):
    pass

class SteinClient:
    def __init__(self, buname: str, *, session: httpx.AsyncClient):
        self._session, self._buname = session, buname
        self._api_key: str | None = None
        self._headers: dict[str, str] = {}
        self._bu: dict[str, Any] | None = None

    async def _init_headers(self) -> None:
        if self._api_key:
            return
        r = await self._session.get(BASE_URL)
        m = re.search(r'<script type="module" crossorigin src="([\w/.-]+)"></script>', r.text)
        js = await self._session.get(f"{BASE_URL}/{m.group(1)}")
        m2 = re.search(JS_RX, js.text)
        self._api_key = m2.group(1)
        self._headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "x-api-key": self._api_key,
        }

    async def login(self, user: str, pwd: str) -> None:
        await self._init_headers()
        await self._session.post(f"{API_URL}/login_check", json={"username": user, "password": pwd})
        data = (await self._session.get(f"{API_URL}/app/data", headers=self._headers)).json()
        self._bu = next(bu for bu in data["bus"] if bu["name"] == self._buname)

    async def async_get_assets(self) -> List[Dict[str, Any]]:
        url = f"{API_URL}/assets?buIds={self._bu['id']}"
        return (await self._session.get(url, headers=self._headers)).json()

STATUS_MAP = {
    "ready": "Einsatzbereit",
    "semiready": "Bedingt einsatzbereit",
    "notready": "Nicht einsatzbereit",
    "inuse": "Im Einsatz",
    "maint": "In Wartung",
}