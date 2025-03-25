from sqlalchemy.orm import Session  
from app.models import User
from app.schemas import UserCreate
from app.core.security import get_password_hash
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas import UserCreate
from app.core.security import hash_password
from app.auth import get_current_user
#Create the new user
def createuser(db: Session, user_data: UserCreate): 
    #hashed the user given password
    hashed_password = get_password_hash(user_data.password)  
    #Get the user data and sote in the variable 
    db_user = User(  
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    #Added the user user_data in to databse
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    #get the user given input
    return db_user 

#Get the user by email 
def get_user_by_email(db : Session, email : str):
    return db.query(User).filter(User.email == email).first()

#Get the user by db id
def get_user_by_id(db : Session , id : str):
    return db.query(User).filter(User.id == id).first()

#list all users from db
def list_users(db : Session , skip : int = 0 ,limit : int = 10 ):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "organization":
        raise HTTPException(status_code=403, detail="Only organizations can create users")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        org_id=current_user["org_id"]  # Assigning to logged-in org
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully", "user_id": new_user.id, "org_id": new_user.org_id}
