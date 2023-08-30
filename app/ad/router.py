from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.ad.crud import create_ad
from app.ad.model import Ad
from app.ad.serializer import AdCreate, AdResponse, GetAds
from app.db.session import get_db
from fastapi import Query
from app.controllers.auth import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/create", response_model=AdResponse)
def create_ads(
    ad: AdCreate,
    db: Session = Depends(get_db),
    auth_header=Depends(auth_handler.check_current_user_tokens),
):
    user, _token_dict = auth_header
    return create_ad(db, ad, owner_id=user.get("user_id"))


@router.put("/edit/{ad_id}", response_model=AdResponse)
def edit_ad(
    ad: AdCreate,
    ad_id: int,
    db: Session = Depends(get_db),
    auth_header=Depends(auth_handler.check_current_user_tokens),
):
    user, _token_dict = auth_header
    db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    if db_ad.owner_id != user.get("user_id"):
        raise HTTPException(status_code=401, detail="Ad not belongs to you")
    for key, value in ad.model_dump().items():
        setattr(db_ad, key, value)
    db.commit()
    db.refresh(db_ad)
    return db_ad


@router.delete("/delete/{ad_id}")
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    auth_header=Depends(auth_handler.check_current_user_tokens),
):
    user, _token_dict = auth_header
    db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    if db_ad.owner_id != user.get("user_id"):
        raise HTTPException(status_code=401, detail="Ad not belongs to you")
    db.delete(db_ad)
    db.commit()
    return {"message": "Ad deleted successfully"}


@router.get("/list", response_model=List[GetAds])
def list_ads(
    skip: int = Query(0, alias="page"), limit: int = 10, db: Session = Depends(get_db)
):
    ads = db.query(Ad).options(joinedload(Ad.comments)).offset(skip).limit(limit).all()
    return ads


@router.get("/user_ads", response_model=List[GetAds])
def list_ads(
    skip: int = Query(0, alias="page"),
    limit: int = 10,
    db: Session = Depends(get_db),
    auth_header=Depends(auth_handler.check_current_user_tokens),
):
    user, _token_dict = auth_header
    ads = (
        db.query(Ad)
        .options(joinedload(Ad.comments))
        .filter(Ad.owner_id == user.get("user_id"))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return ads
