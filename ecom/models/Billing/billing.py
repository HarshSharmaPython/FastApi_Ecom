from pydantic import BaseModel, Field,EmailStr
from typing import List,Optional
from beanie import Document,before_event,Update,Link
from datetime import datetime


class BillingProduct(BaseModel):
    product_id : Link["VariantProduct"] | Link["SimpleProduct"]= Field()
    quantity: int
    regular_price: float
    sale_price: float


class BillingCustomer(BaseModel):
    coustomer_name: str  = Field(default=None)
    coustomer_address: str  = Field(default=None)
    coustomer_phone:str = Field(default=None)
    coustomer_email: EmailStr = Field()

class BillType(BaseModel):
    bill_srno: int 
    bill_date: datetime = Field(default = None)
    bill_amount: float
    customer : BillingCustomer  = Field(default=None)
    product: list[BillingProduct] = Field(default=[])
class Bill(Document,BillType):
    class Settings:
        name = "bill"
