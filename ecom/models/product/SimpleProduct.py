from enum import Enum
from pydantic import BaseModel, Field
from beanie import Document, Link
from datetime import datetime
from ..TimeStamp import TimeStamps
from .Category import Category
from typing import Dict

class SaleType(BaseModel):
    sale_price: float = Field(default=0, ge=0)
    start_date: datetime | None = Field(default=None)
    end_date: datetime | None = Field(default=None)

class TaxType(BaseModel):
    is_tax_applied: bool = Field(default=False)
    tax_amount: float | None = Field(default=None)

class QuantityType(BaseModel):
    allow_back_order: bool = Field(default=False)
    quantity: int = Field(default=0)

class Enum_type(str, Enum):
    Serum="serum"
    Moisturizer="moisturizer"
    tablet="tablet"

class Filter(BaseModel):
    tags:list[str]
    brand:str
    age:int
    type_of_product:Enum_type=Field(default=Enum_type.Moisturizer) 


class Description(BaseModel):
    long_desc: str
    short_desc: str

class StatusEnum(str, Enum):
    live = "live"
    unlisted = "unlisted"
    private = "private"

GroupType = Dict[str, list[Link["SimpleProduct"]]]

class SimpleProductType(BaseModel):
    name: str
    description: Description
    is_virtual_product: bool = Field(default=False)
    category: list[Link[Category]] = Field(default=[])
    regular_price: float
    sale: SaleType | None = Field(default=None)
    sku_number: int
    allow_back_order: bool = Field(default=False)
    tax: TaxType
    images: list[str] | None = Field(default=None)
    status: StatusEnum = Field(default=StatusEnum.private)
    slug: str
    meta_title: str
    meta_description: str
    grouped_with: GroupType = Field(default={})
    filters:Filter

class SimpleProduct(Document, SimpleProductType, TimeStamps):
    type: str = Field(default='simple')
    class Settings: 
        name = "product"


class UpdateProductType(BaseModel):
    name: str | None = Field(default=None)
    description: Description | None = Field(default=None)
    is_virtual_product: bool | None = Field(default=None)
    category: list[Link[Category]] | None = Field(default=None)
    regular_price: float | None = Field(default=None)
    sale: SaleType | None = Field(default=None)
    sku_number: int | None = Field(default=None)
    allow_back_order: bool = Field(default=False)
    tax: TaxType | None = Field(default=None)
    images: list[str] | None = Field(default=None)
    status: StatusEnum | None = Field(default=None)
    grouped_with: GroupType | None = Field(default=None)
    slug: str
    meta_title: str
    meta_description: str

class MassCreateSimpleProduct(BaseModel):
    name: str
    is_virtual_product: bool | None= Field(default=False)
    description: Description | None = Field(default=Description(long_desc="", short_desc=""))
    category: list[Link[Category]] | None = Field(default=None)
    regular_price: float | None = Field(default=0)
    sku_number: int | None = Field(default=-1)
    quantity_details: QuantityType | None = Field(default=QuantityType(allow_back_order=False, quantity=0))
    tax: TaxType | None = Field(default=TaxType(is_tax_applied=False, tax_amount=0))
    images: list[str] | None = Field(default=None)
    status: StatusEnum | None = Field(default=StatusEnum.private)
    slug: str | None = Field(default="")
    meta_title: str | None = Field(default="")
    meta_description: str = Field(default="")
