from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.config import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password :str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    # Correct way to set expiration
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # ✅ Corrected

    expire = datetime.utcnow() + expires_delta  # ✅ Now it's a timedelta object
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
