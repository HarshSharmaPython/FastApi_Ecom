from pydantic import BaseModel, Field, EmailStr
from beanie import Document,before_event,Update,Link


class CreateMail(BaseModel):
    subject : str= Field(default=None)
    body: str= Field(default=None)



class Maildetail(BaseModel):
    email_address: str= Field(default=None)
    password : str= Field(default=None)



class Mail(Document,CreateMail):
    class Settings:
        name = "other"

class NewMail(Document,Maildetail):
    class Settings:
        name = "other"
        