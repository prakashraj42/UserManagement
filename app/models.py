from sqlalchemy import Column, String, Integer, ForeignKey,Boolean
from app.database import Base
from sqlalchemy.orm import relationship
import random
import string


def generate_unique_id(length = 10):

    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters,k=length))

class Organization(Base):

    __tablename__ = "organizations"
    
    id = Column (Integer, primary_key=True, index=True)
    org_id = Column(String(10), default=generate_unique_id(), unique= True)
    orgname = Column(String, index = True , nullable =True)
    email = Column(String, unique = True, index = True, nullable = True)
    hashed_password  = Column(String, nullable = True)
    firstname = Column(String, index = True , nullable =True)
    lastname = Column(String, index = True , nullable =True)
    mobileno = Column(String, index = True , nullable =True)
    country = Column(String, index = True , nullable =True)
    otp_verified = Column(Boolean, default=False)

    users = relationship("User", back_populates="organization")


class User(Base):

    __tablename__ = "users"

    id = Column (Integer, primary_key=True, index=True)
    username = Column(String, index = True, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password  = Column(String, nullable = False)
    org_id = Column(String, ForeignKey("organizations.org_id"))

    organization = relationship("Organization", back_populates="users")








    