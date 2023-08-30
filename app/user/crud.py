from sqlalchemy.orm import Session
from app.user.model import User
from app.controllers.auth import AuthHandler

auth_handler = AuthHandler()


def create_user(db: Session, user: User):
    hashed_password = auth_handler.generate_hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
