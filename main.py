import csv
import time
import random

from shopee_api import extract_ids, fetch_pdp

def parse_product(data: dict) -> dict:
    item = data["data"]["item"]

    result = {
        "item_id": item["item_id"],
        "shop_id": item["shop_id"],
        "name": item["title"],
        "price": item["price"] / 100000,
        "price_before_discount": item["price_before_discount"] / 100000,
    }

    pb = data["data"].get("price_breakdown")
    result["price_after_voucher"] = (
        pb.get("price", {}).get("single_value", 0) / 100000
        if pb else None
    )

    return result

def main():
    with open("link.csv", encoding="utf-8") as f:
        links = [r["link"] for r in csv.DictReader(f)]

    for idx, link in enumerate(links, 1):
        try:
            print(f"[{idx}] {link}")

            itemid, shopid = extract_ids(link)
            raw = fetch_pdp(itemid, shopid)
            product = parse_product(raw)

            print(product)

        except Exception as e:
            print(f"[ERROR] {link} | {e}")

        time.sleep(random.randint(3, 6))

if __name__ == "__main__":
    main()
