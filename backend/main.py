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

# class UserCreate(BaseModel):
#     email: str
#     password: str
#     contact_num : Optional[int] = None
#     company : Optional[str] = None
#     name : Optional[str] = None
#     is_member : Optional[bool] = False
#     role : Optional[str] = None

    
#     @validator('*', pre=True)
#     def escape_html(cls, value):
#         if isinstance(value, str):
#             return html.escape(value)
#         return value


# class UserResponse(BaseModel):
#     email: str
#     company: Optional[str]
#     is_member: Optional[bool]
#     contact_num: Optional[str]
#     name: Optional[str]
#     role: Optional[str]

#     @validator('*', pre=True)
#     def escape_html(cls, value):
#         if isinstance(value, str):
#             return html.escape(value)
#         return value


# class LoginRequest(BaseModel):
#     username: str
#     password: str

# @app.get("/email_test")
# def test():
#     send_email()
#     return 
    

@app.get("/init/")
def init_database():
    try:
        init_db()
    except:
        print('DB init error')
    return
    


# @app.get("/auth/get_users/", response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
#     users = db.query(User).all()
#     return users

# @app.post("/register/")
# def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    
#     # escaped_data = {key: html.escape(value) if isinstance(value, str) else value for key, value in user.dict().items()}
    
#     # sanitized_user = UserCreate(**escaped_data)

#     sanitized_user = user

#     existing_user = db.query(User).filter(User.email == sanitized_user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     hashed_password = hash_password(user.password)

#     new_user = User(
#         email=sanitized_user.email, 
#         password_hash=hashed_password,
#         contact_num=sanitized_user.contact_num,
#         company=sanitized_user.company,
#         name=sanitized_user.name,
#         is_member=sanitized_user.is_member,
#         role=sanitized_user.role
#         )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     # email notification service using AWS SES
#     try:
#         send_email(user_data = new_user)
#     except HTTPException as e:
#         print(f"Error sending email: {e.detail}")

#     return {"msg": "User registered successfully", "email": user.email}

# @app.post("/login")
# def login_user(response: Response, request: LoginRequest, db: Session = Depends(get_db_session)):
#     user = db.query(User).filter(User.email == request.username).first()
#     pw_check = verify_password(request.password, user.password_hash)
#     if not user or not pw_check:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     token = create_jwt_token(user.email)

#     #CSRF protection by cookie to check if the JWT is being sent by the same domain
#     response.set_cookie(
#             key="access_token",
#             value=token,
#             httponly=True,  
#             samesite="Lax",  
#             secure=True , 
#         )

#     print(token)

#     return {"msg": "Login successful", "token": token}

# @app.post("/token")
# def login_user(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session) ):
#     user = db.query(User).filter(User.email == request.username).first()
#     pw_check = verify_password(request.password, user.password_hash)
#     if not user or not pw_check:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     token = create_jwt_token(user.email)

#     #CSRF protection by cookie to check if the JWT is being sent by the same domain
#     response.set_cookie(
#             key="access_token",
#             value=token,
#             httponly=True,  
#             samesite="Lax",  
#             secure=True  
#         )

#     print(token)

#     return {"access_token": token, 'token_type': 'bearer'}


