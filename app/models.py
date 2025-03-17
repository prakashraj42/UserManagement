from sqlalchemy import Column, String, Integer
from app.database import Base

class user(Base):

    __tablename__ = "user"

    id = Column (Integer, primary_key=True, index=True)
    username = Column(String, index = True, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password  = Column(String, nullable = False)
