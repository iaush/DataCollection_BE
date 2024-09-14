from fastapi import Depends, HTTPException, status, Response, FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from typing import Optional, List
from src.database.database import SessionLocal, init_db, get_db_session
from src.models.user import User
from src.services.loginService import hash_password, verify_password, create_jwt_token, get_current_user
from src.services.emailService import send_email
from src.services.middlewareService import RateLimitter, XSSMiddleware
from src.routers.user import router as user_router
from src.routers.auth import router as auth_router
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
import html

app = FastAPI()
app.add_middleware(RateLimitter, max_requests=3, time_window=5)
app.add_middleware(XSSMiddleware)


app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/email_test", description="Send a test email")
def test():
    send_email()
    return 

@app.get("/init/", description="Initialize the database if starting a new database instance")
def init_database():
    try:
        init_db()
    except:
        print('DB init error')
    return
    




