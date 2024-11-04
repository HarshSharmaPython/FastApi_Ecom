from pydantic import BaseModel,Field
from beanie import Document
from datetime import datetime,timezone
from enum import Enum
from ..TimeStamp import TimeStamps


class TicketStatus(str,Enum):
    Open = "Open"
    Closed = "Closed"


class CreateTicket(BaseModel):
    Name : str = Field(default=None)
    Phone: str= Field(default=None)
    Email: str= Field(default=None)
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    
    
class UpdateTicket(BaseModel):
    title : str = Field(default=None)
    description : str = Field(default=None)
    status : TicketStatus = Field(default=None)



class Ticket(Document,CreateTicket,TimeStamps):
    status : TicketStatus = Field(default="Open")
    class Settings:

        name = "tickets"
        
        