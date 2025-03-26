from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.core.security import create_access_token, verify_password
from app.models import Organization

auth = APIRouter()

@auth.post("/token")
def org_admin_login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):

    org = db.query(Organization).filter(Organization.email == form_data.username).first()
    print (form_data.username)
    print (org.email)
    if not org:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Organization not found")

    if not verify_password(form_data.password, org.hashed_password):  
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = create_access_token(data={"sub": org.email, "role": "organization", "org_id": org.id})

    return {"access_toke" : access_token, "token_type": "bearer"}