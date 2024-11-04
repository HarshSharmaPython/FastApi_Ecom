from pydantic import BaseModel, Field
from beanie import Link
from .Category import Category

class FilterSimpleProductType(BaseModel):
    category: list[Link[Category]] = Field(default=[])