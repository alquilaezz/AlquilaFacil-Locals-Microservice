from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------- LocalCategory ----------

class LocalCategoryOut(BaseModel):
    id: int
    name: str
    photo_url: Optional[str]

    class Config:
        orm_mode = True

# ---------- Local ----------

class LocalBase(BaseModel):
    local_name: str
    description: Optional[str] = None
    country: str
    city: str
    district: str
    street: str
    price_per_hour: int
    capacity: int
    features: Optional[str] = None
    local_category_id: int

class LocalCreate(LocalBase):
    photo_urls: Optional[List[str]] = None  # para crear LocalPhoto

class LocalUpdate(BaseModel):
    local_name: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    price_per_hour: Optional[int] = None
    capacity: Optional[int] = None
    features: Optional[str] = None
    local_category_id: Optional[int] = None
    photo_urls: Optional[List[str]] = None

class LocalOut(LocalBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    photos: List[str]

    class Config:
        orm_mode = True

# ---------- Comment ----------

class CommentCreate(BaseModel):
    local_id: int
    text: str
    rating: int

class CommentOut(BaseModel):
    id: int
    user_id: int
    local_id: int
    text: str
    rating: int

    class Config:
        orm_mode = True
