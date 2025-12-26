import requests
import random
import re

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Mobile Safari/537.36"
    ),
    "accept": "application/json",
    "x-api-source": "pc",
    "referer": "https://shopee.vn/"
}

def extract_ids(link: str):
    """
    https://shopee.vn/...-i.123456.987654
    """
    match = re.search(r'i\.(\d+)\.(\d+)', link)
    if not match:
        raise ValueError("Cannot extract itemid/shopid")
    return match.group(1), match.group(2)

def fetch_pdp(itemid: str, shopid: str) -> dict:
    url = "https://shopee.vn/api/v4/pdp/get_pc"

    params = {
        "itemid": itemid,
        "shopid": shopid
    }

    r = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=10
    )

    r.raise_for_status()
    return r.json()