from pydantic import BaseModel

class Base(BaseModel):
    name: str
    description: str

class Create(Base):
    pass

class Blog(Base):
    id: int

    class Config:
        orm_mode = True
