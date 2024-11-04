from pydantic import BaseModel, Field
from beanie import Document

from ..TimeStamp import TimeStamps



class CreateBanner(BaseModel):
    imageLink : str | None = Field(default=None)
    redirectLink : str | None = Field(default=None)




class UpdateBanner(BaseModel):
    imageLink : str | None = Field(default=None)
    redirectLink : str | None = Field(default=None)
    
class Banner(Document,CreateBanner, TimeStamps):
    
    class Settings:
        name = "banner"