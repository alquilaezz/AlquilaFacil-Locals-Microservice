from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/api/v1/local-categories", tags=["LocalCategories"])

@router.get("", response_model=list[schemas.LocalCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.LocalCategory).all()
