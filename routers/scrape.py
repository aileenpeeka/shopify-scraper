from fastapi import APIRouter, HTTPException, Query
from services.extractor import extract_multiple_sites
from models.schema import BrandContext
from typing import Any

router = APIRouter()

@router.get("/scrape", response_model=Any)
def scrape_shopify_store(
    website_url: str = Query(..., description="Shopify store URL"),
    include_competitors: bool = Query(False, description="Also scrape competitors")
):
    try:
        return extract_multiple_sites(website_url, include_competitors=include_competitors)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") 