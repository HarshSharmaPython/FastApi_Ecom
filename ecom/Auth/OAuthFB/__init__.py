from fastapi import APIRouter, HTTPException, Depends

FBAuth = APIRouter()

@FBAuth.get('/')
async def FBOpenAuthIndex():
    return {'message':'mail open auth by FB routing'}