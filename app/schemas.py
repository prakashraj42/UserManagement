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

    id : int
    email: EmailStr
    orgname : str


class LoginRequest(BaseModel):
    email : str
    password: str


class OrgTokenResponse(BaseModel):

    org_id : str
    access_token :str
    token_type: str

class UserTokenResponse(BaseModel):
    pass