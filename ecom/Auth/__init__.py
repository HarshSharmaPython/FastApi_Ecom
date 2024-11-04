from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from .mail import MailAuth
from .OAuthFB import FBAuth
from .mail.service import decode_jwt_token, checkUserExist,generate_referral_code,checkreferal
from ..config import Config

oauth2_scheme = OAuth2PasswordBearer(Config.OAuth_Token_URL)
Auth = APIRouter(tags=["Auth"])

@Auth.get('/')
async def MailAuthIndex():
    return {'message':'this is auth including all the auth route'}

Auth.include_router(MailAuth, prefix='/mailauth',tags=['Mail Auth'])
Auth.include_router(FBAuth, prefix="/fbauth",tags=['FBAuth'])


@Auth.get('/get-current-user')
async def Profile(token: str = Depends(oauth2_scheme)):
    user = decode_jwt_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="no user found")     
    return user