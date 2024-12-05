import random
from threading import Thread
from urllib import request

from requests import get


def test_api(idx: int):
    lang = random.choice(["fa", "en"])
    resp = get(
        "http://127.0.0.1:8000", params={"idx": idx}, headers={"Accept-Language": lang}
    )
    resp.raise_for_status()
    print(
        f"Lang: {lang} ID: {resp.json()['idx']} Text: {resp.json()['text']} FOR: {idx}"
    )


for thread in [Thread(target=test_api, args=[i]) for i in range(100)]:
    thread.start()
