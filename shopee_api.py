import requests
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
    match = re.search(r'i\.(\d+)\.(\d+)', link)
    if not match:
        raise ValueError("Cannot extract itemid/shopid")
    return match.group(1), match.group(2)

def fetch_pdp(itemid: str, shopid: str) -> dict:
    url = "https://shopee.vn/api/v4/pdp/get_pc"
    params = {"itemid": itemid, "shopid": shopid}

    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def parse_product(data: dict) -> dict:
    item = data["data"]["item"]
    pb = data["data"].get("price_breakdown")

    return {
        "item_id": item["item_id"],
        "shop_id": item["shop_id"],
        "name": item["title"],
        "price": item["price"] / 100000,
        "price_before_discount": item["price_before_discount"] / 100000,
        "price_after_voucher": (
            pb.get("price", {}).get("single_value", 0) / 100000
            if pb else None
        )
    }