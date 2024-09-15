from fastapi import FastAPI
from src.database.database import SessionLocal, init_db, get_db_session
from src.services.emailService import send_email
from src.services.middlewareService import RateLimitter, XSSMiddleware
from src.routers.user import router as user_router
from src.routers.auth import router as auth_router
import html

#initialize app and add middleware
app = FastAPI()
app.add_middleware(RateLimitter, max_requests=3, time_window=5)
app.add_middleware(XSSMiddleware)

#routes for different types of operations
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])



#general test routes / initialization routes
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
    




