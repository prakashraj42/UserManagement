from pydantic import BaseModel , EmailStr

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str


class UserResponse(BaseModel):

    id : int
    username : str
    email : str


class OrganizationCreate(BaseModel):

    orgname  : str
    email: EmailStr
    password : str
    firstname : str
    lastname : str
    country : str
    mobileno : str

class OrganizationResponse(BaseModel):

    id : str
    email: EmailStr
    orgname : str


