from fastapi import APIRouter, HTTPException, Depends, status
from ..models import CreateInventory,Invenrtory,UpdateInventory
from beanie import PydanticObjectId
from datetime import datetime,timezone


Manager = APIRouter(tags=["Manager"])

@Manager.post("/")
async def create_inventory(inverotry:CreateInventory):
    to_add = Invenrtory(**inverotry.model_dump())
    await to_add.insert()
    return to_add



@Manager.get("/allinventory")
async def get_all_inventory():
    return await Invenrtory.find().to_list()



@Manager.get("/inventory")
async def get_inventory(id:PydanticObjectId):
    return await Invenrtory.find_one({"_id":id})

@Manager.delete("/")
async def delete_inventory(id:PydanticObjectId):
    to_delete = await Invenrtory.find_one({"_id":id})
    if to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Inventory not found")
    await to_delete.delete()
    return {"message":"Inventory deleted"}

@Manager.delete("/")
async def delete_all_inventory():
    to_delete = await Invenrtory.find().to_list()
    if to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Inventory not found")
    await to_delete.delete()
    return {"message":"Inventory deleted"}


@Manager.put("/update")
async def update_inventory(id:PydanticObjectId,inventory:UpdateInventory):
    to_update = await Invenrtory.find_one({"_id":id})
    if to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Inventory not found")
    updated_product = inventory.product_id if inventory.product_id is not None else to_update.product_id
    await to_update.set({**inventory.model_dump(exclude_none= True,exclude=["product_id"]),"updated_at":datetime.now(timezone.utc),"product_id":updated_product})
    return to_update
