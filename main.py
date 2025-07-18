from fastapi import FastAPI
from routers.scrape import router
from database import Base, engine
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="Shopify Brand Insight Fetcher")

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home():
    if os.path.exists("index.html"):
        return open("index.html").read()
    return "<h2>Shopify Scraper API</h2><p>Try /docs or /api/scrape</p>"

app.include_router(router, prefix="/api") 