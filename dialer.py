import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

# helper to locate resource files both in source and frozen executable


def get_resource_path(name: str) -> Path:
    """Return the path to *name* next to the source file or executable."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / name
    return Path(__file__).with_name(name)


CONFIG_FILE = get_resource_path("config.json")


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file '{CONFIG_FILE.name}' not found. "
            "Copy 'config.example.json' to 'config.json' and set your "
            "API credentials."
        )
    with CONFIG_FILE.open() as f:
        return json.load(f)


EXTENSION_FILE = get_resource_path("extension.txt")


def load_extension() -> str:
    if not EXTENSION_FILE.exists():
        raise FileNotFoundError(
            f"Extension file '{EXTENSION_FILE.name}' not found. "
            "Create it with your extension number."
        )
    return EXTENSION_FILE.read_text().strip()


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
    if number.startswith("tel:"):
        number = urlparse(number).path
    try:
        cfg = load_config()
    except FileNotFoundError:
        print("Missing config.json. Copy config.example.json and fill in your credentials.")
        return 1
    api_key = cfg.get("api_key")
    if not api_key:
        print("Config must contain 'api_key'.")
        return 1
    try:
        origin = load_extension()
    except FileNotFoundError:
        print("Missing extension.txt. Create it with your extension number.")
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
