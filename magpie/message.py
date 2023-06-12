import requests

_bark_token = ""


def set_bark_token(bark_token: str):
    global _bark_token
    _bark_token = bark_token


def bark_send_message(text: str):
    assert _bark_token
    requests.get(f"https://api.day.app/{_bark_token}/{text}", timeout=3)
