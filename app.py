import os
import csv
from fastapi import FastAPI, Query
from shopee_api import extract_ids, fetch_pdp, parse_product

app = FastAPI(title="Shopee Crawler API")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/crawl")
def crawl_one(link: str = Query(...)):
    """
    Crawl 1 sản phẩm Shopee
    """
    itemid, shopid = extract_ids(link)
    raw = fetch_pdp(itemid, shopid)
    product = parse_product(raw)
    return product

@app.get("/crawl-batch")
def crawl_batch():
    """
    Crawl toàn bộ link trong link.csv
    """
    results = []

    with open("link.csv", encoding="utf-8") as f:
        links = [r["link"] for r in csv.DictReader(f)]

    for link in links:
        try:
            itemid, shopid = extract_ids(link)
            raw = fetch_pdp(itemid, shopid)
            product = parse_product(raw)
            results.append(product)
        except Exception as e:
            results.append({"link": link, "error": str(e)})

    return {
        "total": len(results),
        "data": results
    }