from typing import Dict, Set
from pydantic import BaseModel, Field
from beanie import Document, Link
from ..TimeStamp import TimeStamps
from .SimpleProduct import SaleType, QuantityType, StatusEnum, Description, TaxType
from .Category import Category
from datetime import datetime


class Variant(BaseModel):
    name: str
    regular_price: float = Field(default=0, ge=0)
    images: list[str]
    sku_number: int | None = Field(default=None)
    sale: SaleType | None = Field(default=None)
    quantity_details: QuantityType

class VariantType(BaseModel):
    variant: Variant | None = Field(default=None)
    attributes: Dict[str, str]
    is_valid: bool = Field(default=False)

class UpdateVariantType(BaseModel):
    variant: Variant | None = Field(default=None)
    is_valid: bool | None = Field(default=None)

AttributeType = Dict[str, Set[str]]
VariantsType = Dict[str, VariantType]

class VariantProductType(BaseModel):
    name: str
    description: Description
    category: list[Link[Category]] | None = Field(default=None)
    is_virtual_product: bool = Field(default=False)
    status: StatusEnum = Field(default=StatusEnum.private)
    attributes: AttributeType = Field(default={})
    tax: TaxType

class VariantProduct(Document, VariantProductType, TimeStamps):
    variants: VariantsType = Field(default={})
    type: str = Field(default="variant")
    class Settings:
        name="product"

class UpdateVariantProductType(BaseModel):
    name: str | None = Field(default=None)
    description: Description | None = Field(default=None)
    category: list[Link[Category]] | None = Field(default=None)
    is_virtual_product: bool | None = Field(default=None)
    status: StatusEnum | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    tax: TaxType | None = Field(default=None)
