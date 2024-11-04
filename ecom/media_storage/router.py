from fastapi import APIRouter, HTTPException, status, UploadFile, BackgroundTasks
from beanie import PydanticObjectId
from ..models import Media, Folder
from .service import delete_folders_and_their_content, delete_media_files
from . import upload_image
from beanie.operators import In

MediaRouter = APIRouter(tags=["Media"])

@MediaRouter.get('/', )
async def GetFilesAndFolders(folder: PydanticObjectId | None = None):
    try:
        media = await Media.find(Media.parent==folder, Media.is_folder==False).to_list()
        folders = await Folder.find(Media.parent==folder, Media.is_folder==True).to_list()
        return {"media": media, "folders": folders}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@MediaRouter.post('/create-folder', tags=['Media'])
async def CreateNewFolder(name: str, parent: PydanticObjectId  = None):
    if len(name.strip())==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The folder name can't be empty.")
    check_folder_exists = await Folder.find_one(Folder.name==name, Folder.is_folder == True, Folder.parent==parent)
    if check_folder_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The folder with the name <{name}> already exists in this directory.")
    try:
        folder = Folder(name=name, parent=parent)
        insertedFolder = await folder.insert()
        return insertedFolder
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create new folder. Please try again later.")

@MediaRouter.post('/upload-files', )
async def CreateUploadFiles(files: list[UploadFile], parent: PydanticObjectId = None, alt: str = None):
    if len(files)==0 or (files[0].size==0 and files[0].filename==""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files are provided.")
    try:
        insertedMedias = []
        for file in files:
            response = await upload_image(file, folder="dynamic_data")
            media = Media(parent=parent, alt=alt, imgSrc=response['url'], name=response['name'], size=response['size'])
            insertedMedia = await media.insert()
            insertedMedias.append(insertedMedia)
        return insertedMedias
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to upload the files. Please try again later.")

@MediaRouter.patch('/move-media', )
async def MoveFiles(files_and_folders: list[PydanticObjectId], new_parent: PydanticObjectId = None):
    if new_parent:
        check_if_new_folder_exists = await Folder.find_one(Folder.id==new_parent, Folder.is_folder==True)
        if not check_if_new_folder_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The folder in which the files have to be moved does not exists.")
    try:
        await Media.find(In(Media.id, files_and_folders)).update({"$set": {Media.parent: new_parent}})
        return {"message": "Successfully moved all the files and folders to the destination."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to move the files. Please try again later.")

@MediaRouter.delete('/delete-files', )
async def DeleteMediaFiles(files: list[PydanticObjectId], background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(delete_media_files, files)
        return {"message": "Successfully deleted the files."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to delete the files. Please try again later.")
        
@MediaRouter.delete('/delete-folders', )
async def DeleteFolders(folder_ids: list[PydanticObjectId], background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(delete_folders_and_their_content, folder_ids)
        return {"message": "Successfully deleted the folder and all its content."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to delete the folder. Please try again later.")

