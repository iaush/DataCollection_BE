from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.database.database import SessionLocal, init_db, get_db_session
from src.models.user import User
from src.services.loginService import hash_password, verify_password

app = FastAPI()


class UserCreate(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def test():
    return 'OKAY'
    

@app.get("/init/")
def init_database():
    try:
        init_db()
    except:
        print('DB init error')
    return
    


@app.get("/users/")
def get_users(db: Session = Depends(get_db_session)):
    users = db.query(User).all()
    return users

@app.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)

    new_user = User(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "email": user.email}

@app.post("/login/")
def login_user(request: LoginRequest, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"msg": "Login successful", "email": user.email}

