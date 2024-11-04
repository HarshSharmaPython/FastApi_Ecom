from pydantic import BaseModel, Field
from beanie import Document,before_event,Update,Link
from datetime import datetime,timezone
from typing import List
from ..TimeStamp import TimeStamps


class ItemDetail(BaseModel):
    product_id: Link["VariantProduct"]| Link["SimpleProduct"]
    quantity: int
    price: float

class PurchaseItem(BaseModel):
    user_id: Link["User"]
    items: List[ItemDetail] = Field(default=[])
    total: float = 0.0
    purchase_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


   



class Purchase(Document,PurchaseItem,TimeStamps):
    class Settings:
        name = "Purchase"





