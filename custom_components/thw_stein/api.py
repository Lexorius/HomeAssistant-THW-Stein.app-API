"""Simple async client for Stein.APP API using Bearer token."""
from __future__ import annotations
from typing import Any, Dict, List
import logging
from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)

class SteinError(Exception):
    """Raised on API errors."""


class SteinClient:
    BASE_URL = "https://stein.app/api/api/ext"

    def __init__(self, bu_id: int, api_key: str, session: ClientSession):
        self._bu_id = bu_id
        self._session = session
        self._headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": f"Bearer {api_key}",
        }

    async def async_get_assets(self) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/assets/?buIds={self._bu_id}"
        async with self._session.get(url, headers=self._headers) as resp:
            if resp.status != 200:
                raise SteinError(f"Asset list HTTP {resp.status}")
            return await resp.json()

    async def async_get_asset_detail(self, asset_id: int) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/assets/{asset_id}"
        async with self._session.get(url, headers=self._headers) as resp:
            if resp.status != 200:
                raise SteinError(f"Asset {asset_id} HTTP {resp.status}")
            return await resp.json()
