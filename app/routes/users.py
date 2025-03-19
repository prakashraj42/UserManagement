from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import get_user_by_email, createuser ,get_user_by_id , list_users
from app.core.security import verify_password, create_access_token


router = APIRouter()

#Create the user registeration 
@router.post("/register/", response_model=UserResponse)
#Get the usercreate schema and get the input from users
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    #Check if the user already exist in our db 
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ID already exists")
    
    #call the create user function from crud.py
    new_user = createuser(db, user)
    
    #If the user input wrong data return error
    if not new_user:
        raise HTTPException(status_code=500, detail="User creation failed")
    #Return the user input data
    return new_user


#get the user by email 
@router.get("/user/{user_mail}", response_model= UserResponse ,description= "get the user by email")
def get_user(user_mail : str, db: Session = Depends(get_db)):
    #call the get user function from crud.py and depends from database.py
    user = get_user_by_email(db, user_mail) 
    
    #check the user are in the data base if not retun the error
    if user is None:
        raise HTTPException(status_code= 404 , detail= "User Not Found")
    #Return the successfull mesg
    return user


#get the user by email 
@router.get("/user/{user_id}" , response_model= UserResponse , description=  "get the user by userid" )
def get_user(user_id : int, db : Session = Depends(get_db)):
    #call the get user function from crud.py and depends from database.py
    user = get_user_by_id(db, user_id)
    
    #check the user are in the data base if not retun the error
    if user is None:
        raise HTTPException(status_code=404 , detail= "User not found")
    #Return the successfull mesg
    return user


#list users
@router.get("/users/", response_model=list[UserResponse])
def listing_users(skip: int = 0, limit: int= 10 , db :Session =Depends(get_db)):
    users = list_users(db , skip=skip , limit=limit)
    return users


#delete user
@router.delete("/user/", response_model= dict)
def deleting_user(user_id : int , db :Session = Depends(get_db)):
    
    #get given id users from db
    users = get_user_by_id(db,user_id)
    
    #check if the are in the database
    if not users:
        raise HTTPException(status_code=404 , detail= "user not found")
    
    #delete the db
    db.delete(users)
    #commit the latest change
    db.commit()
    #return the successful msg
    return {"msg" : "User deleted Successfully"}

