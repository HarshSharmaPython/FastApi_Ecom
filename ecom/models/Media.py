from pydantic import Field, BaseModel
from beanie import Document, PydanticObjectId
from .TimeStamp import TimeStamps

class Folder(Document, TimeStamps):
    is_folder: bool = Field(default=True)
    parent: PydanticObjectId | None = Field(default=None)
    name: str
    class Settings: 
        name = "media"

class Media(Document, TimeStamps):
    imgSrc: str
    parent:  PydanticObjectId | None = Field(default=None)
    is_folder: bool = Field(default=False)
    name: str
    size: float
    alt: str | None = Field(default=None)
    class Settings: 
        name = "media"

class CollectionMediaProject(BaseModel):
    imgSrc: str
    alt: str | None
