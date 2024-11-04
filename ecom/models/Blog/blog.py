from pydantic import BaseModel, Field, EmailStr
import pymongo
from beanie import Document,before_event,Update
from datetime import datetime,timezone
from ..TimeStamp import TimeStamps
from enum import Enum

class BlogStatusEum(str,Enum):
    live = "live"
    unlisted= "unlisted"
    private = "private"

class UpdateBlogType(BaseModel):
    status: BlogStatusEum | None = Field(default = None)
    title: str | None = Field(default = None)
    category : str | None = Field(default = None)
    image : str | None = Field(default=None)
    content: str | None = Field(default = None)
    meta_title: str | None= Field(default= None)
    meta_desc: str | None = Field(default = None)
    slug : str | None= Field(default=None)

class CreateBlogs(BaseModel):
    status: BlogStatusEum =  Field(default=BlogStatusEum.live)
    title: str = Field(min_length=3, max_length=50)
    category : str = Field(min_length= 3, max_length = 50)
    image:str
    content: str = Field(min_length=3, max_length=5000)
    meta_title: str | None= Field(default= None)
    meta_desc: str | None = Field(default = None)
    slug : str | None= Field(default=None)
    
class Blog(Document,CreateBlogs, TimeStamps):    
    class Settings:
        name = "blogs"
        indexes = [
            [
            ("title", pymongo.TEXT),
            
        ]
    ]
