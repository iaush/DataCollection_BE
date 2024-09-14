from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from src.database.database import get_db_session
from src.models.user import User
from src.services.loginService import hash_password, get_current_user, encrypt_phone_number, decrypt_phone_number
from src.services.emailService import send_email
from src.schemas import UserCreate, UserResponse
from typing import List

router = APIRouter()



@router.post("/register_user/", description="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    
    # escaped_data = {key: html.escape(value) if isinstance(value, str) else value for key, value in user.dict().items()}
    # sanitized_user = UserCreate(**escaped_data)

    sanitized_user = user

    existing_user = db.query(User).filter(User.email == sanitized_user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    #store hashed password(salted) and encrypted phone number(encrypted for privacy) 
    hashed_password = hash_password(user.password)
    encrypted_contact_num = encrypt_phone_number(str(sanitized_user.contact_num))

    new_user = User(
        email=sanitized_user.email, 
        password_hash=hashed_password,
        contact_num=encrypted_contact_num,
        company=sanitized_user.company,
        name=sanitized_user.name,
        is_member=sanitized_user.is_member,
        role=sanitized_user.role
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # email notification service using AWS SES
    try:
        send_email(user_data = new_user)
    except HTTPException as e:
        print(f"Error sending email: {e.detail}")

    return {"msg": "User registered successfully", "email": user.email}


@router.get("/get_users/", response_model=List[UserResponse], description="Requires authentication, Get all users info from database")
def get_users(db: Session = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    users = db.query(User).all()
    
    #return decrypted phone number if user is authenticated (can further restrict to admin role etc)
    for user in users:
        user.number = decrypt_phone_number(user.contact_num)
        # print(decrypt_phone_number(user.contact_num))

    return users