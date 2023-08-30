from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.ad.crud import create_ad
from app.ad.model import Ad
from app.ad.serializer import AdCreate, AdResponse, GetAds
from app.controllers.auth import AuthHandler
from app.db.session import get_db

router = APIRouter()
auth_handler = AuthHandler()


def get_test_user_token():
    # Simulate the process to get a token for a test user
    # This will depend on your actual authentication implementation
    return "your_test_user_token_here"


@router.post("/create", response_model=AdResponse)
def create_ads(
        ad: AdCreate,
        db: Session = Depends(get_db),
        auth_header=Depends(auth_handler.check_current_user_tokens),
) -> AdResponse:
    """
    Create a new ad.
    """
    print(auth_header)
    user, _token_dict = auth_header
    print(user)
    print(_token_dict)
    return create_ad(db, ad, owner_id=user.get("user_id"))


@router.put("/edit/{ad_id}", response_model=AdResponse)
def edit_ad(
        ad: AdCreate,
        ad_id: int,
        db: Session = Depends(get_db),
        auth_header=Depends(auth_handler.check_current_user_tokens),
) -> AdResponse:
    """
    Edit an existing ad.
    """
    user, _token_dict = auth_header
    db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    if db_ad.owner_id != user.get("user_id"):
        raise HTTPException(status_code=401, detail="Ad not belongs to you")
    for key, value in ad.dict().items():
        setattr(db_ad, key, value)
    db.commit()
    db.refresh(db_ad)
    return db_ad


@router.delete("/delete/{ad_id}")
def delete_ad(
        ad_id: int,
        db: Session = Depends(get_db),
        auth_header=Depends(auth_handler.check_current_user_tokens),
) -> dict:
    """
    Delete an ad.
    """
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
) -> List[GetAds]:
    """
    List all ads.
    """
    ads = db.query(Ad).options(joinedload(Ad.comments)).offset(skip).limit(limit).all()
    return ads


@router.get("/user_ads", response_model=List[GetAds])
def list_user_ads(
        skip: int = Query(0, alias="page"),
        limit: int = 10,
        db: Session = Depends(get_db),
        auth_header=Depends(auth_handler.check_current_user_tokens),
) -> List[GetAds]:
    """
    List ads belonging to the current user.
    """
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
