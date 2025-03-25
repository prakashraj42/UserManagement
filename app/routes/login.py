from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Organization
from app.core.security import verify_password, create_access_token
from app.schemas import OrgTokenResponse
from app.logincroud import authenticate_user


loggin = APIRouter()

@loggin.post("/token", response_model=OrgTokenResponse)
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return authenticate_user(form_data, db)


@loggin.post("/create")





