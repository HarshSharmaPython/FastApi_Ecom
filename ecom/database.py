from motor.motor_asyncio import AsyncIOMotorClient
from .config import Config
from fastapi import FastAPI
from beanie import init_beanie
from .models import User, SimpleProduct, VariantProduct, Category, Media, Folder,Blog,Banner,Invenrtory, Contact,Mail,NewMail,Ticket,Purchase

async def db_lifespan(app: FastAPI):
    app.my_secret_str = 'This is top secret'
    app.mongodb_client = AsyncIOMotorClient(Config.MONGODB_CONNECTION_STRING)
    await set_database(app, Config.DATABASE_NAME)
    yield
    app.mongodb_client.close()

async def set_database(app: FastAPI, name: str):
    app.database = app.mongodb_client.get_database(name)
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        print("Connected to database:", name)

    await init_beanie(database=app.database, document_models=[User, Category, SimpleProduct, VariantProduct, Folder, Media, Blog, Banner, Invenrtory, Contact,Mail,NewMail,Ticket,Purchase])