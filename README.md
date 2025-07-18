# Shopify Brand Insight Fetcher

A FastAPI-based microservice to extract brand context and insights from any public Shopify store.

## Features
- Scrapes product catalog, hero products, policies, FAQs, social handles, contact info, about text, and important links.
- Returns structured JSON for easy integration.
- **Persists scraped store info to SQLite database.**
- **Includes a simple HTML frontend.**
- **Bonus: Competitor analysis with multi-site scrape!**

## Tech Stack
- FastAPI
- BeautifulSoup4 + Requests
- Pydantic
- SQLAlchemy (SQLite)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Test the endpoint:**
   ```bash
   curl -X GET "http://localhost:8000/api/scrape?website_url=memy.co.in"
   ```

4. **Try the frontend:**
   Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## Example Response
```json
{
  "product_catalog": ["T-shirt", "Hoodie"],
  "hero_products": ["Shop Featured Hoodie"],
  "privacy_policy": "...",
  "return_policy": "...",
  "refund_policy": "...",
  "faqs": [
    {"question": "How do I return an item?", "answer": "You can return..."}
  ],
  "social_handles": ["https://instagram.com/brand"],
  "contact_emails": ["support@brand.com"],
  "contact_numbers": ["+1234567890"],
  "about_text": "We are a Shopify brand...",
  "important_links": ["/blog", "/contact"]
}
```

## Database
- Scraped store info is saved to `shopify.db` (SQLite).
- See `database.py` for the schema.

## 📬 Postman Collection
A ready-to-use Postman collection is included for easy API testing and demo.

**How to Use:**
1. Open [Postman](https://www.postman.com/).
2. Click **Import** and select `Shopify-API.postman_collection.json` from the project root.
3. The collection includes:
   - **Scrape Shopify Store with Competitors**: Demonstrates scraping a primary Shopify store and its competitor (bonus feature).
   - You can edit the query parameters to test with any Shopify store and toggle competitor analysis.
4. Run the request and view the full JSON response for both the primary brand and its competitor.

**Collection file:**
```
shopify_scraper/Shopify-API.postman_collection.json
```

---

## License
MIT 