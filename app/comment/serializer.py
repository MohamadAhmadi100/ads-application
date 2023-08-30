from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class PydanticComment(CommentCreate):
    id: int
    ad_id: int
    owner_id: int

    class Config:
        from_attributes = True
