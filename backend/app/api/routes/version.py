"""Build and release metadata endpoint."""

import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(tags=["version"])

BUILD_INFO_FILE = Path(__file__).resolve().parents[4] / "BUILD_INFO.json"
DEV_BUILD_INFO = {
    "version": "0.1.0",
    "build": "dev",
    "commit": "unknown",
}


def get_version_info() -> dict[str, str]:
    """Read metadata embedded in a release bundle, or return development defaults."""
    try:
        payload = json.loads(BUILD_INFO_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return DEV_BUILD_INFO.copy()

    return {
        key: str(payload.get(key, DEV_BUILD_INFO[key]))
        for key in DEV_BUILD_INFO
    }


@router.get("/version")
async def version_info() -> dict[str, str]:
    """Return the version, Actions build number, and source commit."""
    return get_version_info()
