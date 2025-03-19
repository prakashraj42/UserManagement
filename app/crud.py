from sqlalchemy.orm import Session  
from app.models import user 
from app.schemas import UserCreate
from app.core.security import get_password_hash

#Create the new user
def createuser(db: Session, user_data: UserCreate): 
    #hashed the user given password
    hashed_password = get_password_hash(user_data.password)  
    #Get the user data and sote in the variable 
    db_user = user(  
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
    return db.query(user).filter(user.email == email).first()

#Get the user by db id
def get_user_by_id(db : Session , id : str):
    return db.query(user).filter(user.id == id).first()

