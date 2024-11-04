import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "687af3d2c5086978ce8a1663dc4ad4050875a691460faaeb7c0a9dc6e5fda426")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    OAuth_Token_URL = "/auth/mailauth/login"
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    DATABASE_NAME= os.getenv("DATABASE_NAME", "store")
    user_points = 100



class MailConfig:
    Marketing_Mail="marketing@compitcom.com"
    M_Password=os.getenv("Marketing_MAil_Password")

    Contact_Mail="contact@compitcom.com"
    C_Password=os.getenv("Contact_Mail_Password")

    Sales_Mail="sales@compitcom.com"
    S_Password=os.getenv("Sales_Mail_Password")



