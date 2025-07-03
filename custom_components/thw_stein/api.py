"""Async wrapper around the unofficial THW Stein.APP REST‑API.

Highlights
----------
*   Uses **aiohttp** (the library shipped with Home Assistant) – no blocking calls.
*   Extracts the dynamic **X‑API‑KEY** from Stein's frontend JavaScript.
*   Provides two high‑level methods:
    * `login()`
    * `async_get_assets()`
"""
from __future__ import annotations

import re
import logging
from typing import Any, Dict, List

import aiohttp

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://stein.app"
API_URL = f"{BASE_URL}/api/api"

# Regex to find the embedded JS file on the Stein landing page
JS_FILE_RX = r'<script[^>]+type="module"[^>]+src="([^"]+)"'

# Regex to extract the X‑API‑KEY assignment inside that JS
API_KEY_PATTERNS = [
    r'["\']X-API-KEY["\']\s*[:=]\s*["\']([A-Za-z0-9_-]+)["\']',
    r'["\']xApiKey["\']\s*[:=]\s*["\']([A-Za-z0-9_-]+)["\']',
    r'["\']x-api-key["\']\s*[:=]\s*["\']([A-Za-z0-9_-]+)["\']',
]


class SteinError(RuntimeError):
    """Raised for all recoverable errors in the wrapper."""


class SteinClient:
    """Very small async client for the THW Stein.APP API."""

    def __init__(self, buname: str, *, session: aiohttp.ClientSession) -> None:
        self._buname = buname
        self._session = session
        self._headers: dict[str, str] = {}
        self._bu_data: Dict[str, Any] | None = None

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    async def _init_headers(self) -> None:
        """Lazy‑initialise the common headers incl. X‑API‑KEY."""
        if self._headers:
            return  # already set

        # 1) Download Stein landing page & extract JS filename
        async with self._session.get(BASE_URL) as resp:
            html = await resp.text()

        js_match = re.search(JS_FILE_RX, html)
        if not js_match:
            raise SteinError("Could not find JS filename on Stein landing page.")

        js_url = f"{BASE_URL}/{js_match.group(1)}"

        # 2) Download JS & extract X‑API‑KEY
        async with self._session.get(js_url) as resp:
            _LOGGER.debug("Fetching JS: %s → status %s", js_url, resp.status)
            js_code = await resp.text()

        key_match = None
        for pattern in API_KEY_PATTERNS:
            key_match = re.search(pattern, js_code, re.IGNORECASE)
            if key_match:
                break
        if not key_match:
            raise SteinError("X‑API‑KEY not found in Stein JavaScript.")

        self._headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "x-api-key": key_match.group(1),
        }
        _LOGGER.debug("X‑API‑KEY extracted successfully")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    async def login(self, username: str, password: str) -> None:
        """Authenticate against Stein and cache the Business‑Unit data."""
        await self._init_headers()

        # Login
        await self._session.post(
            f"{API_URL}/login_check", json={"username": username, "password": password}
        )

        # Fetch global data incl. list of BUs
        async with self._session.get(f"{API_URL}/app/data", headers=self._headers) as resp:
            data = await resp.json()

        self._bu_data = next(
            (bu for bu in data["bus"] if bu["name"].lower() == self._buname.lower()), None
        )
        if not self._bu_data:
            raise SteinError(f"Business Unit '{self._buname}' not found.")

        _LOGGER.debug("Authenticated as %s, BU‑ID=%s", username, self._bu_data["id"])

    async def async_get_assets(self) -> List[Dict[str, Any]]:
        """Return all assets for the configured Business‑Unit."""
        if self._bu_data is None:
            raise SteinError("Not logged in – call login() first")

        url = f"{API_URL}/assets?buIds={self._bu_data['id']}"
        async with self._session.get(url, headers=self._headers) as resp:
            return await resp.json()