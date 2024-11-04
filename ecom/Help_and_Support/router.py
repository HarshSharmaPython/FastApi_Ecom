from fastapi import APIRouter,HTTPException,status,Query
from ..models import CreateTicket,Ticket,TicketStatus
from beanie import PydanticObjectId
from datetime import datetime,timezone
from beanie.operators import In

TicketRouter = APIRouter(tags=["Ticket"])


@TicketRouter.post("/")
async def genrate__ticket(ticket:CreateTicket):
    to_insert_ticket = Ticket(**ticket.model_dump())
    await to_insert_ticket.insert()
    return {"Message":"This is Second Ticket"}

@TicketRouter.get("/alltickets")
async def get_tickets(status:list[TicketStatus]=Query(None)):
    if status is None:
        return await Ticket.find_all().to_list()
    else:
        return await Ticket.find_many(In(Ticket.status,status)).to_list()
    
