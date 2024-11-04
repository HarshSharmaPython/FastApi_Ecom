from beanie import Document
from pydantic import Field, BaseModel
from ..TimeStamp import TimeStamps

class CategoryType(BaseModel):
    name: str
    image: str | None = Field(default=None)

class UpdateCategory(BaseModel):
    name: str | None = Field(default=None)
    image: str | None = Field(default=None)

class Category(Document, CategoryType, TimeStamps):
    class Settings: 
        name = "category"
