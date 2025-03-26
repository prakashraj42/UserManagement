from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import Organization
import jwt
Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")



def get_password_hash(password :str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    # Correct way to set expiration
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 

    expire = datetime.now(timezone.utc) + expires_delta 
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401 ,detail="token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail= "invalid token")


def get_current_user(token : str = Depends(Oauth2_scheme), db : Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        org_id = payload.get("org_id")

        if email is None or org_id is None:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials")
        
        orgs = db.query(Organization).filter(Organization.org_id == org_id, Organization.email == email).first()

        if orgs is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return orgs
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


