from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.schemas import OrganizationCreate, OrganizationResponse, OrgTokenResponse,OTPVerify
from app.orgcrud import  get_org_by_email, list_org,send_otp, verify_otp,create_organization
from app.core.security import  create_access_token
from datetime import timedelta
from app.config import settings
from app.models import Organization
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


org = APIRouter()

@org.post("/org_otp/")
def send_otp_to_org_register(email : str, db: Session = Depends(get_db)):
    existing_org = db.query(Organization).filter(Organization.email == email).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="Organization already registered.")
    return send_otp(email)

@org.post("/verify-otp/")
def verify_organization_otp(request: OTPVerify,db: Session = Depends(get_db)):
    """Verifies OTP and completes organization registration."""
    verify_otp(request.email, request.otp,db)
    return {"msg": "otp verifyed successfully"}

@org.post("/organization/")
def Create_org(org_data : OrganizationCreate, db : Session = Depends(get_db)):


    if get_org_by_email(db, org_data.email):
        orgs = create_organization(db, org_data)

    return {
        "id": orgs.id,
        "email": orgs.email,
        "orgname": orgs.orgname
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


