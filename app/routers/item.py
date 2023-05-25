from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.db import get_db, engine
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/blog/publish", response_model=schemas.Blog)
def create_blog(
    blog: schemas.Create, 
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    # Your authentication logic here
    return crud.create_blog(db=db, item=blog)

# Implement other CRUD operations (read, update, delete) similarly.


@router.get("/blog/{blog_id}")
async def get_blog(blog_id: int):
    # Implementation to get a blog by its ID
    ...

