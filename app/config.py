import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:prakash@123@localhost/user_db") 
    SECRET_KEY = os.getenv("SECRET_KEY", "!@#$%^&*(123456789)")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ALGORITHM  = os.getenv("ALGORITHM", "HS256")

settings = Settings()

