from pydantic import BaseModel
from typing import List, Optional

class FAQ(BaseModel):
    question: str
    answer: str

class BrandContext(BaseModel):
    product_catalog: List[str]
    hero_products: List[str]
    privacy_policy: Optional[str]
    return_policy: Optional[str]
    refund_policy: Optional[str]
    faqs: Optional[List[FAQ]]
    social_handles: List[str]
    contact_emails: List[str]
    contact_numbers: List[str]
    about_text: Optional[str]
    important_links: List[str] 