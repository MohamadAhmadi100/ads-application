from pydantic import BaseModel


class AdCreate(BaseModel):
    title: str
    content: str


class AdResponse(AdCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class GetComments(BaseModel):
    content: str
    owner_id: int


class GetAds(BaseModel):
    id: int
    title: str
    content: str
    comments: list[GetComments]

    class Config:
        orm_mode = True
