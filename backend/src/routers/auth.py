from fastapi import Depends, HTTPException, APIRouter, Response, status, Request, Form, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from typing import Optional, List
from src.database.database import  get_db_session
from src.models.user import User
from src.services.loginService import hash_password, verify_password, create_jwt_token, get_current_user
from src.schemas import UserCreate, UserResponse, LoginRequest
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
def login_user(response: Response, request: LoginRequest, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == request.username).first()
    pw_check = verify_password(request.password, user.password_hash)
    if not user or not pw_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_jwt_token(user.email)

    #CSRF protection by cookie to check if the JWT is being sent by the same domain
    response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  
            samesite="Lax",  
            secure=True , 
        )

    print(token)

    return {"msg": "Login successful", "token": token}

@router.post("/token")
def login_user(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session) ):
    user = db.query(User).filter(User.email == request.username).first()
    pw_check = verify_password(request.password, user.password_hash)
    if not user or not pw_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_jwt_token(user.email)

    #CSRF protection by cookie to check if the JWT is being sent by the same domain
    response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  
            samesite="Lax",  
            secure=True  
        )

    print(token)

    return {"access_token": token, 'token_type': 'bearer'}