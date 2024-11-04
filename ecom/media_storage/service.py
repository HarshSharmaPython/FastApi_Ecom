from beanie import PydanticObjectId
from ..models import Media, Folder
from ..media_storage import delete_images_with_document
from beanie.operators import In

async def delete_media_files(files: list[PydanticObjectId]):
    try:
        media_to_be_deleted = await Media.find(In(Media.id, files), Media.is_folder==False).to_list()
        await delete_images_with_document(media_to_be_deleted)
    except Exception as e:
        print(e)    

    
async def delete_folder_and_its_content(folder_id: PydanticObjectId):
    await Folder.find_one(Folder.id==folder_id, Folder.is_folder==True).delete_one()
    media_to_be_deleted = await Media.find(Media.parent==folder_id, Media.is_folder==False).to_list()
    stack = await Folder.find(Folder.parent==folder_id, Folder.is_folder==True).to_list()    
    while len(stack)!=0:
        folder = stack.pop()
        child_folders = await Folder.find(Folder.parent==folder.id, Folder.is_folder==True).to_list()
        child_medias = await Media.find(Media.parent==folder.id, Media.is_folder==False).to_list()
        await folder.delete()
        media_to_be_deleted.extend(child_medias)
        stack.extend(child_folders)

    await delete_images_with_document(media_to_be_deleted)

async def delete_folders_and_their_content(folder_id: list[PydanticObjectId]):
    for folder in folder_id:
        await delete_folder_and_its_content(folder)