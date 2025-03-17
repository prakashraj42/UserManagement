from sqlalchemy.orm import Session  
from app.models import user 
from app.schemas import UserCreate
from app.core.security import get_password_hash


def createuser(db: Session, user_data: UserCreate): 
    hashed_password = get_password_hash(user_data.password)  

    db_user = user(  
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.flush()
    db.refresh(db_user)
    print(db.query(user).all())  # Check if any data exists
    return db_user 


def get_user_by_email(db : Session, email : str):
    return db.query(user).filter(user.email == email).first()


