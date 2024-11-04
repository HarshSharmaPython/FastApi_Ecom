# all the routes are here   
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.requests import Request
from beanie import PydanticObjectId
from ..config import Config
from ..Auth import decode_jwt_token
from ..Product.Inventory_management.Product_IM_services import *
from ..models import Contact,Mail,CreateMail,Maildetail,NewMail,Support,Ticket,TicketStatus,CreateTicket,UpdateTicket
from .service import *
from ..media_storage import MediaRouter
from ..Product import ProductRouter
from ..Help_and_Support import TicketRouter
from ..Blog import BlogRouter
from ..Banner import BannerRouter
from ..payment import *


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.OAuth_Token_URL)

def is_admin(request: Request, token: str = Depends(oauth2_scheme)):
    user = decode_jwt_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin: User not found")     
    if user['role'] == "admin":
        request.app.user = user
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin: Not authorized")
    
Admin = APIRouter(dependencies=[Depends(is_admin)], tags=["Admin"])

#router under this will be Admin only

@Admin.get('/')
async def AdminIndex():
    return {'message':'this is message saying hello to the admin'}

@Admin.get('/profile')
async def Profile(request: Request):
    return request.app.user

@Admin.get('/contact')
async def GetContact(id: PydanticObjectId):
    contact = await Contact.get(id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacted response not found")
    return contact

@Admin.get('/contacts')
async def GetAllContacts():
    contacts = await Contact.find_all().to_list()
    return {"data": contacts, "total": len(contacts)}


@Admin.get('/pay')
async def GetPay():
    result=pay()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment response not found")
    return result


@Admin.get('/sucess')
def sucess():
    return "SUCESS"



@Admin.post('/mail')
async def SendMail(mail: CreateMail):
    mail = Mail(**mail.model_dump())
    await mail.insert()
    return {"Message":"Mail Created"}




@Admin.put('/updatemail/{mail_id}')
async def updatemail(mail_id:PydanticObjectId,update:CreateMail):
    mail = await Mail.find_one({'_id':mail_id})
    if mail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail response not found")
    mail.subject= update.subject
    mail.body= update.body
    await mail.save()
    return {"Message":"Mail Updated"}


@Admin.post('/newemail')
async def newemail(email:Maildetail):
    mail = NewMail(**email.model_dump())
    await mail.insert()
    return {"Message":"Mail Created"}

@Admin.put("/newemail/update/{mail_id}")
async def  newemail_update(mail_id:PydanticObjectId,update:Maildetail):
    mail = await NewMail.find_one({'_id':mail_id})
    if mail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail response not found")
    mail.email_address= update.email_address
    mail.password = update.password
    await mail.save()
    return {"Message":"Mail Updated"}


@Admin.get("/tickets")
async def get_tickets():
    tickets = await Ticket.find().to_list(100)
    return tickets

@Admin.put("/tickets/update")
async def update_ticket(ticket_id:PydanticObjectId,update:UpdateTicket):
    ticket = await Ticket.find_one({'_id':ticket_id})
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket response not found")
    ticket.title= update.title
    ticket.description= update.description
    ticket.status= update.status
    await ticket.save()
    return {"Message":"Ticket Updated"}

@Admin.delete("/ticket")
async def delete_ticket(ticket_id:PydanticObjectId):
    ticket = await Ticket.find_one({'_id':ticket_id})
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket response not found")
    await ticket.delete()
    return {"Message":"Ticket Deleted"}





    
Admin.include_router(MediaRouter, prefix="/media")
Admin.include_router(ProductRouter, prefix="/p")
Admin.include_router(BlogRouter, prefix="/blog")
Admin.include_router(BannerRouter, prefix="/banner")
# Admin.include_router(TicketRouter,prefix="/Tickets")
