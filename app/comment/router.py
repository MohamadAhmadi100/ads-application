from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.comment.serializer import CommentCreate, PydanticComment
from app.comment.crud import create_comment
from app.db.session import get_db
from app.controllers.auth import AuthHandler
from app.ad.model import Ad
from app.comment.model import Comment

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/create_comment", response_model=PydanticComment)
def create_comments(
    comment: CommentCreate,
    ad_id: int,
    db: Session = Depends(get_db),
    auth_header=Depends(auth_handler.check_current_user_tokens),
):
    user, _token_dict = auth_header
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    existing_comment = (
        db.query(Comment)
        .filter(Comment.ad_id == ad_id, Comment.owner_id == user.get("user_id"))
        .first()
    )
    if existing_comment:
        raise HTTPException(
            status_code=400, detail="You have already commented on this ad"
        )
    return create_comment(db, comment, ad_id, owner_id=user.get("user_id"))
