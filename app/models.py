from sqlalchemy import Column, String, Integer,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
import random
import string



class User(Base):

    __tablename__ = "user"

    id = Column (Integer, primary_key=True, index=True)
    username = Column(String, index = True, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password  = Column(String, nullable = False)
    org_id = Column(String, ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)

    organization = relationship("Organization", back_populates="users")


def generate_unique_id(length = 10):

    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters,k=length))

class Organization(Base):

    __tablename__ = "organization"

    id = Column(String(10), primary_key=True, index=True, default=generate_unique_id())
    orgname = Column(String, index = True , nullable =False)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password  = Column(String, nullable = False)
    firstname = Column(String, index = True , nullable =False)
    lastname = Column(String, index = True , nullable =False)
    mobileno = Column(String, index = True , nullable =False)
    country = Column(String, index = True , nullable =False)

    users = relationship("User", back_populates="organization")







    