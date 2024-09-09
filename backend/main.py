from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.database.database import SessionLocal, init_db, get_db_session
from src.models.user import User

app = FastAPI()


class UserCreate(BaseModel):
    email: str
    password_hash: str
    role: str

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
    

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    db_user = User(email=user.email, password_hash=user.password_hash, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"email": db_user.email, "id": db_user.id}

@app.get("/users/")
def get_users(db: Session = Depends(get_db_session)):
    users = db.query(User).all()
    return users


