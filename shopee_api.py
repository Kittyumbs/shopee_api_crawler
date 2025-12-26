import requests
import re

HEADERS = {
    # ===== User Agent (desktop web – ổn định hơn mobile) =====
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),

    # ===== Header cơ bản =====
    "accept": "application/json, text/plain, */*",
    "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",

    # ===== Shopee check rất kỹ =====
    "origin": "https://shopee.vn",
    "referer": "https://shopee.vn/",
    "x-api-source": "pc",

    # ===== Fetch headers (bắt chước browser thật) =====
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "sec-ch-ua": '"Chromium";v="126", "Google Chrome";v="126", "Not:A-Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',

    # ===== COOKIE (QUAN TRỌNG NHẤT) =====
    # ❗ THAY GIÁ TRỊ BÊN DƯỚI BẰNG COOKIE CỦA EM
    "cookie": (
        "SPC_F=jGw64AVyWAl4TuSye6PV1O5rQ7O7X0cJ;"
        "SPC_EC=.b3NYQXU0UldDZ2lEb3pQVgrlT8sJK4Fxcv33Jky+lvuURPZMdPcXTNFPLC8n0S5hQ4WdoMZOrfxu7UCquBH8ZRP/ZUOteSAuIqWV/ERIp5uhi3nQByCwlqwGpOxBVIIcydkviDnPBzOfF2/3hCl0osJCyyBZbFf0EURoNIAI0NBBhoRJpVSqrg+ZrgJh4dXANMqcTu4Am8a6eYb/4z0fF6/b0XHxUtcoqn627a+RZJkEgMNhr021I6AYZFc5PhbeC75cpAN+/M01m0o/iAqo62rNIfW4aoN4w6rk9aF852E=;"
        "SPC_U=1352268094;"
        "_fbp=fb.1.1757386214972.90782331940960395;"
        "_gcl_au=1.1.1928023440.1766760602"
    )
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