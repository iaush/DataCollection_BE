from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from src.database.database import SessionLocal, init_db, get_db_session
from src.models.user import User
from src.services.loginService import hash_password, verify_password, create_jwt_token, get_current_user
from src.services.emailService import send_email
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()
# security = HTTPBearer()

class UserCreate(BaseModel):
    email: str
    password: str
    contact_num : Optional[int] = None
    company : Optional[str] = None
    name : Optional[str] = None
    is_member : Optional[bool] = False
    role : Optional[str] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    email: str
    company: Optional[str]
    is_member: Optional[bool]
    contact_num: Optional[str]
    name: Optional[str]
    role: Optional[str]

    class Config:
        orm_mode = True
class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/email_test")
def test():
    send_email()
    return 
    

@app.get("/init/")
def init_database():
    try:
        init_db()
    except:
        print('DB init error')
    return
    


@app.get("/get_users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
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

    # email notification service using AWS SES
    try:
        send_email(user_data = new_user)
    except HTTPException as e:
        print(f"Error sending email: {e.detail}")

    return {"msg": "User registered successfully", "email": user.email}

@app.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == request.username).first()
    pw_check = verify_password(request.password, user.password_hash)
    if not user or not pw_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_jwt_token(user.email)
    print(token)

    return {"msg": "Login successful", "token": token}

@app.post("/token")
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == request.username).first()
    pw_check = verify_password(request.password, user.password_hash)
    if not user or not pw_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_jwt_token(user.email)
    print(token)

    return {"access_token": token, 'token_type': 'bearer'}


