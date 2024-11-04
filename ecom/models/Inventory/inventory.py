from pydantic import BaseModel, Field, EmailStr
import pymongo
from typing import List,Optional
from beanie import Document,before_event,Update,Link
from datetime import datetime,timezone
from ..TimeStamp import TimeStamps
from enum import Enum



class CreateInventory(BaseModel):
    Batch_No: str = Field(default=None)
    product_id: Link["VariantProduct"] | Link["SimpleProduct"]= Field()
    entry_date: datetime | None = Field(default = None)
    mgf_date: datetime | None = Field(default = None)
    exp_date : datetime | None = Field(default = None)
    note : str | None= Field(default=None)
    quantity: int = Field(ge=0,default=0)



class UpdateInventory(BaseModel):
    Batch_No: str = Field(default=None)
    product_id: Link["VariantProduct"] | Link["SimpleProduct"]= Field()
    entry_date: datetime | None = Field(default = None)
    mgf_date: datetime | None = Field(default = None)
    exp_date : datetime | None = Field(default = None)
    note : str | None= Field(default=None)
    quantity: int = Field(ge=0,default=0)
    

class Invenrtory(Document,CreateInventory,TimeStamps):
    class Settings:
        name ="Invetory"
