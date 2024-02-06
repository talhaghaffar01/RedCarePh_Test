from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    product_number: Optional[str]
    reference_drug: Optional[str]
    brand_name: Optional[str]
    active_ingredients: Optional[List[dict]]
    reference_standard: Optional[str]
    dosage_form: Optional[str]
    route: Optional[str]
    marketing_status: Optional[str]

class ProcessedData(BaseModel):
    application_number: Optional[str]
    sponsor_name: Optional[str]
    products: Optional[List[Product]]

