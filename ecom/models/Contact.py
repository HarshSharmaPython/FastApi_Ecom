from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from .TimeStamp import TimeStamps
from enum import Enum

class PreferredContactOptionEnum(str, Enum):
    email = "email"
    phone = "phone"

class ContactType(BaseModel):
    email: EmailStr
    first_name: str = Field(min=1)
    last_name: str = Field(min=1)
    phone: str
    city: str
    preferred_contact_option: PreferredContactOptionEnum = Field(default=PreferredContactOptionEnum.email)
    message: str
    appointment_reason: str 
    appointment_guests: int = Field(min=0, default=0)

class Contact(Document, ContactType, TimeStamps):
    class Settings:
        name = "contact"