"""Async wrapper for THW Stein API – API‑Key only mode."""
from __future__ import annotations
import aiohttp, logging, re
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://stein.app"
API_BASE = f"{BASE_URL}/api/api/ext"

class SteinError(RuntimeError):
    pass

class SteinClient:
    def __init__(self, buname: str, *, api_key: str, session: aiohttp.ClientSession):
        self._buname = buname
        self._api_key = api_key
        self._session = session
        self._headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "x-api-key": api_key,
        }
        self._bu: Dict[str, Any] | None = None

    async def login(self) -> None:
        """Validate the API‑Key and cache Business Unit."""
        async with self._session.get(f"{API_BASE}/app/data", headers=self._headers) as resp:
            if resp.status != 200:
                raise SteinError(f"API key invalid (status {resp.status})")
            data = await resp.json()

        self._bu = next((bu for bu in data["bus"] if bu["name"].lower() == self._buname.lower()), None)
        if not self._bu:
            raise SteinError(f"Business unit '{self._buname}' not found.")
        _LOGGER.debug("API key valid, BU id=%s", self._bu["id"])

    async def async_get_assets(self) -> List[Dict[str, Any]]:
        if not self._bu:
            raise SteinError("Client not logged in.")
        url = f"{API_BASE}/assets?buIds={self._bu['id']}"
        async with self._session.get(url, headers=self._headers) as resp:
            return await resp.json()
