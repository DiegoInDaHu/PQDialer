import json
import os
import sys
from pathlib import Path

import requests

CONFIG_FILE = Path(__file__).with_name('config.json')


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file '{CONFIG_FILE.name}' not found. "
            "Copy 'config.example.json' to 'config.json' and set your "
            "API credentials."
        )
    with CONFIG_FILE.open() as f:
        return json.load(f)


def make_call(api_key: str, origin: str, number: str) -> str:
    url = f"https://vpbx.me/api/originatecall/{origin}/{number}"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: dialer.py <phone_number>")
        return 1
    number = argv[1]
    try:
        cfg = load_config()
    except FileNotFoundError:
        print("Missing config.json. Copy config.example.json and fill in your credentials.")
        return 1
    api_key = cfg.get("api_key")
    origin = cfg.get("origin")
    if not api_key or not origin:
        print("Config must contain 'api_key' and 'origin'.")
        return 1
    try:
        result = make_call(api_key, origin, number)
        print("Call initiated:", result)
    except requests.HTTPError as exc:
        print("Failed to initiate call:", exc.response.text)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
