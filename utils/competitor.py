def guess_competitor_urls(brand_url: str) -> list[str]:
    domain = brand_url.replace("https://", "").replace("http://", "").split("/")[0]
    keywords = domain.split(".")[0]  # e.g., 'allbirds'

    # Basic hardcoded map (expand as needed)
    known_sets = {
        "allbirds": ["https://www.nike.com", "https://www.adidas.com", "https://www.rothys.com"],
        "memy": ["https://snitch.co.in", "https://huedee.com"]
    }

    competitors = known_sets.get(keywords, [])
    return competitors[:1] if competitors else [] 