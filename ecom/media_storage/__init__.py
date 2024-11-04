import cloudinary
import cloudinary.uploader
from ..config import Config
from fastapi import UploadFile
from ..models import Media

# Configuration       
cloudinary.config( 
    cloud_name = Config.cloud_name,
    api_key = Config.api_key,
    api_secret = Config.api_secret, # Click 'View Credentials' below to copy your API secret
    secure=True
)

async def upload_image(image: UploadFile, folder: str):
    upload_result = cloudinary.uploader.upload(image.file, folder=folder)
    return {"name": upload_result["public_id"], "url": upload_result["secure_url"], "size": upload_result['bytes']/1024}
   
def delete_image(images: list[Media]):
    try:
        for image in images:
            cloudinary.uploader.destroy(image.name)
    except Exception as e:
        print(e)

async def delete_images_with_document(images: list[Media]):
    try:
        for image in images:
            cloudinary.uploader.destroy(image.name)
            await image.delete()
    except Exception as e:
        print(e)


from .router import MediaRouter

