import bcrypt
import jwt
import datetime
from src.models.user import User
from fastapi import HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

key = SECRET_KEY.encode()


cipher_suite = Fernet(key)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def encrypt_phone_number(phone_number: str):
    return cipher_suite.encrypt(phone_number.encode('utf-8'))

def decrypt_phone_number(encrypted_phone_number: bytes)-> str:
    return cipher_suite.decrypt(encrypted_phone_number).decode('utf-8')

def create_jwt_token(email: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=4)  # Default expiration time
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
def get_current_user(request: Request):

    token = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
    if not token:
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = decode_jwt_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return email
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail="Wrong / invalid credentials")
    
