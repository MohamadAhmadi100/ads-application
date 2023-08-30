from sqlalchemy.orm import Session
from app.comment.model import Comment
from app.comment.serializer import CommentCreate


def create_comment(db: Session, comment: CommentCreate, ad_id: int, owner_id: int):
    db_comment = Comment(**comment.model_dump(), ad_id=ad_id, owner_id=owner_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
