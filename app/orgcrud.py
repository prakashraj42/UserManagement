from app.schemas import OrganizationCreate
from app.models import Organization
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_password_hash

def create_org(db: Session, request : OrganizationCreate):
    hashed_password = get_password_hash(request.password)  

    org_data = Organization(
        email = request.email,
        orgname = request.orgname,
        firstname = request.firstname,
        lastname = request.lastname,
        hashed_password = hashed_password,
        mobileno = request.mobileno,
        country = request.country

    )

    db.add(org_data)
    db.commit()
    db.refresh(org_data)
    return org_data


def get_org_by_email(db : Session, email : str):
    return db.query(Organization).filter(Organization.email == email).first()


