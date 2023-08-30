from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.user.crud import create_user
from app.user.serializer import UserCreate, UserResponse, UserLogin
from app.controllers.auth import AuthHandler
from app.user.model import User
from app.db.session import get_db

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    sub_dict = {"user_id": db_user.id, "user_email": db_user.email}
    response.headers["access_token"] = auth_handler.encode_access_token(sub_dict)
    response.headers["refresh_token"] = auth_handler.encode_refresh_token(sub_dict)
    return db_user


@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None or not auth_handler.verify_password(
        user.password, db_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    sub_dict = {"user_id": db_user.id, "user_email": db_user.email}
    response.headers["access_token"] = auth_handler.encode_access_token(sub_dict)
    response.headers["refresh_token"] = auth_handler.encode_refresh_token(sub_dict)
    return {"email": db_user.email}
