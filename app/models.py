from sqlalchemy import Column, Integer, String
from app.db import Base

class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)


class Auth(Base):
    __tablename__ = "auth"

    username = Column(String, primary_key=True, index=True)
    password = Column(String)


