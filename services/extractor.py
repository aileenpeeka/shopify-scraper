import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.schema import BrandContext, FAQ
import re

def extract_shopify_insights(url: str) -> BrandContext:
    if not url.startswith("http"):
        url = "https://" + url
    try:
        homepage = requests.get(url, timeout=8)
        if homepage.status_code != 200:
            raise ValueError("Website not reachable")
    except requests.Timeout:
        raise ValueError("Timeout while connecting to website")
    except:
        raise ValueError("Invalid URL")

    soup = BeautifulSoup(homepage.text, "lxml")

    # Product catalog
    try:
        products_resp = requests.get(urljoin(url, "/products.json"), timeout=8).json()
        product_catalog = [p['title'] for p in products_resp.get("products", [])]
    except requests.Timeout:
        product_catalog = []
    except:
        product_catalog = []

    # Hero products
    hero_products = []
    for tag in soup.find_all(["a", "h2", "h3"]):
        if tag and tag.text and any(kw in tag.text.lower() for kw in ["buy", "shop", "featured"]):
            hero_products.append(tag.text.strip())

    # Policy links
    def extract_policy(term):
        link = soup.find("a", string=lambda x: x and term.lower() in x.lower())
        if link:
            try:
                page = requests.get(urljoin(url, link['href']), timeout=8)
                psoup = BeautifulSoup(page.text, "lxml")
                return psoup.get_text(separator=" ", strip=True)[:300]
            except requests.Timeout:
                return None
            except:
                return None
        return None

    # Contact info
    contact_emails = list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", homepage.text)))
    contact_numbers = list(set(re.findall(r"\+?\d[\d -]{8,12}\d", homepage.text)))

    # Social links
    social_links = re.findall(r"https?://(?:www\.)?(instagram|facebook|tiktok|linkedin)\.com/[^\s\"'>]+", homepage.text)

    # FAQs
    faqs = []
    for q in soup.find_all(["h3", "strong", "p"]):
        if "?" in q.text and len(q.text) < 200:
            next_tag = q.find_next_sibling()
            if next_tag:
                faqs.append(FAQ(question=q.text.strip(), answer=next_tag.text.strip()))

    # About Text
    about_text = ""
    about = soup.find("a", string=lambda x: x and "about" in x.lower())
    if about:
        try:
            page = requests.get(urljoin(url, about['href']), timeout=8)
            about_soup = BeautifulSoup(page.text, "lxml")
            about_text = about_soup.get_text(separator=" ", strip=True)[:500]
        except requests.Timeout:
            pass
        except:
            pass

    # Useful Links
    links = soup.find_all("a", href=True)
    useful = []
    for link in links:
        if any(kw in link.text.lower() for kw in ["blog", "track", "order", "contact"]):
            useful.append(link['href'])

    # Save to DB
    try:
        from database import SessionLocal, Store
        db = SessionLocal()
        store = Store(
            url=url,
            product_count=len(product_catalog),
            contact_email=contact_emails[0] if contact_emails else "",
            about_text=about_text
        )
        db.add(store)
        db.commit()
        db.close()
    except Exception as e:
        pass  # Optionally log DB errors

    return BrandContext(
        product_catalog=product_catalog,
        hero_products=hero_products,
        privacy_policy=extract_policy("privacy"),
        return_policy=extract_policy("return"),
        refund_policy=extract_policy("refund"),
        faqs=faqs,
        social_handles=social_links,
        contact_emails=contact_emails,
        contact_numbers=contact_numbers,
        about_text=about_text,
        important_links=useful,
    )

def extract_multiple_sites(primary_url: str, include_competitors=False):
    all_data = {"primary": extract_shopify_insights(primary_url)}

    if include_competitors:
        from utils.competitor import guess_competitor_urls
        competitors = guess_competitor_urls(primary_url)
        all_data["competitors"] = {}

        for comp_url in competitors:
            print(f"Scraping: {comp_url}")
            try:
                all_data["competitors"][comp_url] = extract_shopify_insights(comp_url)
            except Exception as e:
                all_data["competitors"][comp_url] = {"error": f"Failed to fetch: {str(e)}"}

    return all_data 