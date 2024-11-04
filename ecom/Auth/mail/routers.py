from fastapi import APIRouter, HTTPException, Depends, status
from .service import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ...models import RegisterUser, User
from ...config import Config



oauth2_scheme = OAuth2PasswordBearer(Config.OAuth_Token_URL)


MailAuth = APIRouter()





# Route for user registration
@MailAuth.post('/register', status_code=status.HTTP_201_CREATED)
async def MailAuthIndex(user_create: RegisterUser):
    userExists = await checkUserExist(user_create.email)
    refExists = await checkreferal(user_create.referral_by)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Register User: with email already registered.")
    
    if refExists or user_create.referral_by==None:
        user =  User(**user_create.model_dump(),referral_code = generate_referral_code())
        user.password = hash_password(user.password)

        # if refExists:
        #     refExists.points += Config.user_points
        #     await refExists.save()
    
        await user.insert()
        return {"message": "Successfully created the user."}

# Route for user login
@MailAuth.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    userExists = await checkUserExist(form_data.username)
    print(form_data.username)
    if not userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login User: user does not exists")

    if not verify_password(form_data.password, userExists.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login User: incorrect password")

    access_token = create_access_token(data={"email": userExists.email, "id": str(userExists.id), "name": userExists.name, "role": userExists.role})
    return {"access_token": access_token, "token_type": "bearer"}






