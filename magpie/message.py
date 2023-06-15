import asyncio
import os

import requests

try:
    from telegram import Bot
    from telegram.request import HTTPXRequest
except ImportError:
    Bot = None
    HTTPXRequest = None

_bark_token = ""
_telegram_token = ""
_telegram_chat_id = 0


def set_bark_token(token: str):
    global _bark_token
    _bark_token = token


def setup_telegram(token: str, chat_id: int):
    assert Bot
    global _telegram_token, _telegram_chat_id
    _telegram_token = token
    _telegram_chat_id = chat_id


def bark_send_message(text: str):
    assert _bark_token
    requests.get(f"https://api.day.app/{_bark_token}/{text}", timeout=3)


def telegram_send_message(text: str):
    assert Bot
    assert _telegram_token
    assert _telegram_chat_id
    request = None
    for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]:
        if proxy_url := os.environ.get(key):
            request = HTTPXRequest(proxy_url=proxy_url)
    asyncio.run(
        Bot(token=_telegram_token, request=request).send_message(
            chat_id=_telegram_chat_id, text=text
        )
    )
