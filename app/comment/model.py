from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    ad_id = Column(Integer, ForeignKey("ads.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    ad = relationship("Ad", back_populates="comments")
    owner = relationship("User", back_populates="comments")
