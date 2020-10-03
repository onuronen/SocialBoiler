from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime as dt
from sqlalchemy import(
    Column,
    Boolean,
    String,
    Integer,
    Float,
    DateTime,
    JSON,
    ARRAY,
    ForeignKey
)

Base = declarative_base()

class User_Credentials(Base):
    __tablename__ = "user_credentials"
    email = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    auth_token = Column(String, nullable=True)
    

class Profile_Page(Base):
    __tablename__ = "profile_page"
    email = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    age = Column(String, nullable=True)
    about = Column(String, nullable=True)


if __name__ == "__main__":
    pass