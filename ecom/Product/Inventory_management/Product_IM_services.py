from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import CollectionInvalid

async def db_create_collection(database: AsyncIOMotorDatabase, name: str):
    try:
        await database.create_collection(name)
        return True
    except CollectionInvalid:
        return False

async def db_get_collections(database: AsyncIOMotorDatabase):
    return await database.list_collection_names()