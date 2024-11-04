from pydantic import BaseModel, Field, EmailStr
import pymongo
from beanie import Document, before_event, Update,Link
from .TimeStamp import TimeStamps
from typing import List
from enum import Enum
from datetime import datetime, timezone



class UserRoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class RegisterUser(BaseModel):
    name: str
    password: str
    email: EmailStr
    referral_by : str | None =Field(default=None)



class Cart(BaseModel):
    Product_id : Link["VariantProduct"]| Link["SimpleProduct"]
    quantity : int = 1


class User(Document, RegisterUser, TimeStamps):
    role: UserRoleEnum = Field(default=UserRoleEnum.user)
    cart: List[Cart]= Field(default=[])
    favorites:List[Link["VariantProduct"] | Link["SimpleProduct"]]= Field(default=[])
    Purchase: List = Field(default=[])
    referral_code : str
    referral_to : List =Field(default=[])
    points : int = Field(default=0)
    has_purchased : bool = Field(default=False)

    
    class Settings:
        name = "users"
        indexes = [
            [
                ('email', pymongo.TEXT)
            ]
        ]

    @before_event(Update)
    def user_updated(self):
        self.updated_at = datetime.now(timezone.utc)













+

class UpdateUser(BaseModel):
    name:  str | None = Field(default = None)
    email: str | None = Field(default=None)
    quantiy : int
    cart: List[Cart]= Field(default=[])
    Purchase: List = Field(default=[])
    favorites:List[Link["VariantProduct"] | Link["SimpleProduct"]]= Field(default=[])



  
        