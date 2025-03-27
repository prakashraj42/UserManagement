from app.schemas import OrganizationCreate
from app.models import Organization
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_password_hash
from app.email import send_org_reg_mail,generate_otp
from app.redis import set_otp,get_otp,delete_otp
from fastapi import HTTPException

# def create_org(db: Session, request : OrganizationCreate):
      
#     otp= generate_otp()
#     set_otp(request.email, otp)  # Store OTP in Redis
#     send_org_reg_mail(request.email,otp)

#     return {"msg": "OTP sent to email. Please verify."}


def create_organization(db: Session, request:Organization):

    hashed_password = get_password_hash(request.password)
    
    org = Organization(
        orgname=request.orgname,
        firstname=request.firstname,
        lastname=request.lastname,
        hashed_password=hashed_password,
        mobileno=request.mobileno,
        country=request.country
    )

    db.add(org)
    db.commit()
    db.refresh(org)
    return org

def send_otp(email: str):
    """Generates and sends OTP to the given email."""
    otp = generate_otp()
    set_otp(email, otp)  # Store OTP in Redis
    send_org_reg_mail(email, otp)
    return {"msg": "OTP sent to email. Please verify before completing registration."}

def verify_otp(email: str, otp: str, db:Session):
    """Verifies OTP for a given email."""
   
    stored_otp = get_otp(email)  # Get OTP using email
    print(f"User input OTP: {otp}, Stored OTP: {stored_otp}")

    if not stored_otp:
        raise HTTPException(status_code=401, detail="OTP expired or invalid")
    
    if stored_otp != otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    delete_otp(otp)

    org = db.query(Organization).filter(Organization.email == email).first()

    if not org:
        # Organization not found → Create it now
        org = Organization(email=email, otp_verified=True)
        db.add(org)
    else:
        # Organization found → Update OTP verification status
        org.otp_verified = True

    db.commit()
    db.refresh(org)

    return {"msg": "OTP verified successfully!", "email": email, "otp_verified": org.otp_verified}

# def verify_otp(email:str, otp:str, db:Session, request: OrganizationCreate):

#     store_otp = get_otp(email)
#     if not store_otp:
#         raise  HTTPException(status_code=401, detail="Opt expired or invalid")
    
#     if set_otp != otp:
#         raise HTTPException(status_code=401, detail="Invalid Otp")
    
#     delete_otp(email)

#     hashed_password = get_password_hash(request.password)
#     org_data = Organization(
#         email = request.email,
#         orgname = request.orgname,
#         firstname = request.firstname,
#         lastname = request.lastname,
#         hashed_password = hashed_password,
#         mobileno = request.mobileno,
#         country = request.country

#     )

#     db.add(org_data)
#     db.commit()
#     db.refresh(org_data)

#     return org_data


def get_org_by_email(db : Session, email : str):
    return db.query(Organization).filter(Organization.email == email, Organization.otp_verified==True).first()


def list_org(db : Session , skip : int = 0 ,limit : int = 10 ):
    return db.query(Organization).offset(skip).limit(limit).all()