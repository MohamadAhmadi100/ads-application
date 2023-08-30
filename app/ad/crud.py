from sqlalchemy.orm import Session
from app.ad.model import Ad
from app.ad.serializer import AdCreate


def create_ad(db: Session, ad: AdCreate, owner_id: int):
    db_ad = Ad(**ad.model_dump(), owner_id=owner_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad
