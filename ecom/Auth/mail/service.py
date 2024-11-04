from ...config import Config
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Optional
from ...models import User
import bcrypt
import random
import string

async def checkUserExist(email):
    user = await User.find_one(User.email==email)
    return user


def generate_referral_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase+ string.digits,k=length))

async def checkreferal(code:str):
    return await User.find_one({"referral_code": code})

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return {"email": payload.get("email"), "name": payload.get("name"), "id": payload.get("id"), "role": payload.get("role")}
    except InvalidTokenError:
        return None

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))