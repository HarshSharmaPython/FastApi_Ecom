from fastapi import FastAPI, HTTPException, status
from .Auth import Auth
from .User import UserRouter
from .Admin import Admin
from .Manager import Manager
from .database import db_lifespan
from .Blog import get_blog, get_all_blogs
from .Help_and_Support import TicketRouter
from .Shop import ShopRouter
from fastapi.middleware.cors import CORSMiddleware
from .models import ContactType, Contact, Media, Folder, CollectionMediaProject
from beanie import PydanticObjectId
from starlette import status

app = FastAPI(tags=[], lifespan=db_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/" )
def read_root():
    return {"message": "Your app is working properly"}

@app.get('/blogs')
async def fetch_blogs():
    return await get_all_blogs(status=['live'])

@app.get("/blog")
async def fetch_blog(blog_id: str):
    blog = await get_blog(blog_id)
    if blog.status == "live":
        return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")

@app.post('/contact')
async def create_new_contact(contact: ContactType):
    try:
        c = Contact(**contact.model_dump())
        await c.insert()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Please try again later.")
    return {"message": "Successfully submitted the details."}

@app.get('/collections')
async def get_all_collection_media(collection_name: str):
    folder = await Folder.find_one(Folder.name==collection_name, Folder.parent==PydanticObjectId("66859f2b2dd2d8ed6a6bfe3d"), Folder.is_folder==True)
    if folder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found.")
    media = await Media.find_many(Media.parent==folder.id, Media.is_folder==False).project(CollectionMediaProject).to_list()    
    return media

@app.get('/collection')
async def get_collection(collection_name: str, look_no: int):
    folder = await Folder.find_one(Folder.name==collection_name, Folder.parent==PydanticObjectId("66859f2b2dd2d8ed6a6bfe3d"), Folder.is_folder==True)
    print(folder)
    if folder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found.")
    media = await Media.find(Media.parent==folder.id, Media.is_folder==False, limit=2, skip=look_no-1).project(CollectionMediaProject).to_list()    
    if len(media)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Look not found.")
    return {"look": media[0], "next": len(media)==2}

app.include_router(Auth, prefix="/auth")
app.include_router(UserRouter, prefix="/user")
app.include_router(Admin, prefix="/admin")
app.include_router(Manager, prefix="/manager")
app.include_router(ShopRouter,prefix="/shop")
app.include_router(TicketRouter,prefix="/help_and_support")
