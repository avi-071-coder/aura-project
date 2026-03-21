from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from urllib.parse import urlparse
import time

from app.services.scraper import scrape_text
from app.services.ai_engine import generate_summary

router = APIRouter()

cache = {}
CACHE_TTL = 300

read_stats = {}

class Anchor(BaseModel):
    text: str
    selector: str

class SummarizeRequest(BaseModel):
    url: str
    time_spent: int = 0

class SummarizeResponse(BaseModel):
    summary: str
    bullets: List[str]
    estimated_read_time: str
    anchors: List[Anchor]
    community_avg: float
    visits: int

@router.post("/summary", response_model=SummarizeResponse)
def summarize_url(request: SummarizeRequest):
    now = time.time()

    parsed = urlparse(request.url)
    if not parsed.scheme or not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")

    if request.url in cache:
        data, ts = cache[request.url]
        if now - ts < CACHE_TTL:
            update_stats(request.url, request.time_spent)
            attach_stats(data, request.url)
            return data

    scrape = scrape_text(request.url)
    result = generate_summary(scrape["text"], scrape["html"])

    update_stats(request.url, request.time_spent)
    attach_stats(result, request.url)

    cache[request.url] = (result, now)
    return result


def update_stats(url, time_spent):
    if url not in read_stats:
        read_stats[url] = {"visits": 0, "avg_time": 0}

    stats = read_stats[url]

    if time_spent > 0:
        total = stats["avg_time"] * stats["visits"]
        stats["visits"] += 1
        stats["avg_time"] = round((total + time_spent) / stats["visits"], 2)
    else:
        stats["visits"] += 1


def attach_stats(result, url):
    result["community_avg"] = read_stats[url]["avg_time"]
    result["visits"] = read_stats[url]["visits"]