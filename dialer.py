import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests


def get_config_file() -> Path:
    """Return path to ``config.json`` preferring an external copy."""
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.argv[0]).resolve().parent
        external = exe_dir / "config.json"
        if external.exists():
            return external
        bundle_dir = Path(getattr(sys, "_MEIPASS", exe_dir))
        return bundle_dir / "config.json"
    return Path(__file__).with_name("config.json")


def load_config():
    config_file = get_config_file()
    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file '{config_file.name}' not found. "
            "Copy 'config.example.json' to 'config.json' and set your "
            "API credentials and extension."
        )
    with config_file.open() as f:
        return json.load(f)


def make_call(api_key: str, extension: str, number: str) -> str:
    """Initiate a click-to-call from *extension* to *number*."""
    url = f"https://vpbx.me/api/originatecall/{extension}/{number}"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }
    params = {"timeout": 20, "autoAnswer": "true"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: dialer.py <phone_number>")
        return 1
    number = argv[1]
    if number.startswith("tel:"):
        number = urlparse(number).path
    try:
        cfg = load_config()
    except FileNotFoundError:
        print("Missing config.json. Copy config.example.json and fill in your credentials.")
        return 1
    api_key = cfg.get("api_key")
    extension = cfg.get("extension")
    if not api_key:
        print("Config must contain 'api_key'.")
        return 1
    if not extension:
        print("Config must contain 'extension'.")
        return 1
    try:
        result = make_call(api_key, extension, number)
        print("Call initiated:", result)
    except requests.HTTPError as exc:
        print("Failed to initiate call:", exc.response.text)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
