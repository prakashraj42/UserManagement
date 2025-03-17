from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import get_user_by_email, createuser
from app.core.security import verify_password, create_access_token


router = APIRouter()

@router.post("/register/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Received registration request: {user.dict()}")  # Debug

    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ID already exists")
    
    new_user = createuser(db, user)
    
    print(f"Created user: {new_user}")  # Debug

    if not new_user:
        raise HTTPException(status_code=500, detail="User creation failed")

    return new_user

