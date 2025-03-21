from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.schemas import OrganizationCreate, OrganizationResponse
from app.orgcrud import create_org, get_org_by_email
from app.core.security import verify_password, create_access_token


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

