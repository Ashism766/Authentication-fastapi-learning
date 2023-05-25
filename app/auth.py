from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models import Auth
from sqlalchemy.orm import Session

app = APIRouter()


# JWT Configurations
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_access_token(username):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": username,
        "exp": datetime.utcnow() + access_token_expires
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str, db: Session):
    User = db.query(Auth).filter(Auth.username == username).first()
    return User

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)

    if not user:
        print("is it here")
        return False
    if not verify_password(password, user.password):
        return False
    return user



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/register")
def register_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    user = db.query(Auth).filter(Auth.username == username).first()
    

    if user:
        raise HTTPException(status_code=400, detail="Username already exists")


    new_user = Auth(username = username, password = get_password_hash(password))
    print(user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful", "access_token":generate_access_token(username), "token_type":"bearer"}



    
@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    print("form data", form_data.username, form_data.password)
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
