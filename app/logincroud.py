


from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User, Organization
from app.core.security import verify_password, create_access_token
from app.schemas import OrgTokenResponse

def authenticate_user(form_data, db: Session) -> OrgTokenResponse:
    # Check if it's an Organization Admin
    org = db.query(Organization).filter(Organization.email == form_data.username).first()
    if org and verify_password(form_data.password, org.password_hash):
        access_token = create_access_token({"org_id": org.id, "role": "organization"})
        return OrgTokenResponse(access_token=access_token, token_type="bearer", role="organization")
    
    # Check if it's a Normal User
    user = db.query(User).filter(User.email == form_data.username).first()
    if user and verify_password(form_data.password, user.hashed_password):
        access_token = create_access_token({"user_id": user.id, "org_id": user.org_id, "role": "user"})
        return OrgTokenResponse(access_token=access_token, token_type="bearer", role="user")

    raise HTTPException(status_code=400, detail="Invalid credentials")
