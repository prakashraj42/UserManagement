from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.schemas import OrganizationCreate, OrganizationResponse, OrgTokenResponse
from app.orgcrud import create_org, get_org_by_email, list_org
from app.core.security import  create_access_token
from datetime import timedelta
from app.config import settings
from app.models import Organization
from passlib.context import CryptContext
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


org = APIRouter()

@org.post("/organization/", response_model=OrganizationResponse)
def Create_organization(org_data : OrganizationCreate, db : Session = Depends(get_db)):
    if get_org_by_email(db, org_data.email):
        raise HTTPException(status_code= 404, detail= "Email already exists")
    
    orgs = create_org(db, org_data)

    return {
        "id": orgs.id,
        "email": orgs.email,
        "orgname": orgs.orgname,  
        "msg": "organization created successfully"
    }

@org.delete("/organization")
def delete_organization(email: str, db : Session = Depends(get_db)):

    orgs = get_org_by_email(db, email)

    if not orgs:
        raise HTTPException(status_code=404, detail= " org not found")
    
    db.delete(orgs)
    db.commit()
    return "success"
    

@org.get("/orgs/", response_model=list[OrganizationResponse])
def listing_org(skip: int = 0, limit: int= 10 , db :Session = Depends(get_db)):
    orgs = list_org(db , skip=skip , limit=limit)
    return orgs


