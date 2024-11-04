from fastapi import APIRouter, HTTPException, status
from ..models.Banner import CreateBanner,Banner,UpdateBanner
from beanie import PydanticObjectId




BannerRouter = APIRouter(tags=["Banner"])

@BannerRouter.post("/",)
async def CreateBanner(banner:CreateBanner):
    to_insert_banner = Banner(**banner.model_dump())
    await to_insert_banner.insert()
    return {"message":"Banner Created"}

@BannerRouter.get("/banner")
async def get_banner(banner_id:PydanticObjectId):
    banner = await Banner.get(banner_id)
    if banner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Banner not found")
    return banner

@BannerRouter.get("/allbanner")
async def get_all_banner():
    banner = await Banner.find_many().to_list()
    return banner

@BannerRouter.delete("/")
async def delete_banner(banner_id:PydanticObjectId):
    banner = await Banner.find_one({"_id":banner_id})
    if banner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Banner not found")
    await banner.delete()
    return {"Message":"Banner is Deleted"}


@BannerRouter.put("/update/{banner_id}")
async def update_banner(banner_id: PydanticObjectId, updated_banner: UpdateBanner):
    banner = await Banner.find_one({"_id": banner_id})
    if banner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found")

   
    banner.imageLink= updated_banner.imageLink
    banner.redirectlink = updated_banner.redirectlink
    await banner.save()

    return {"message": "Banner updated successfully"}